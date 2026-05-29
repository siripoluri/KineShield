import time
from typing import Any, Dict

from kineshield.feasibility.collision_checker import check_collision_risk
from kineshield.feasibility.ik_checker import check_ik_reachability
from kineshield.feasibility.timing_checker import check_timing_feasibility
from kineshield.feasibility.workspace_checker import check_workspace_bounds
from kineshield.repair.repair_policy import repair_action
from kineshield.verdict.verdict_schema import FeasibilityVerdict


class FeasibilityChecker:
    """Baseline feasibility checker for structured robot actions."""

    def __init__(
        self,
        max_reach_m: float = 1.2,
        workspace_bounds=((-1.0, 1.0), (-1.0, 1.0), (0.0, 1.2)),
    ) -> None:
        self.max_reach_m = max_reach_m
        self.workspace_bounds = workspace_bounds

    def check(self, action: Dict[str, Any]) -> FeasibilityVerdict:
        start = time.perf_counter()

        action_id = str(action.get("action_id", "unknown"))
        action_type = str(action.get("action_type", "unknown"))
        target_pose = action.get("target_pose", {})
        position = target_pose.get("position", action.get("target_position", [0.0, 0.0, 0.0]))
        constraints = action.get("constraints", {})

        checks = [
            check_workspace_bounds(position, self.workspace_bounds),
            check_ik_reachability(position, self.max_reach_m),
            check_collision_risk(action),
            check_timing_feasibility(
                float(action.get("estimated_duration_s", 1.0)),
                float(constraints.get("max_duration_s", 3.0)),
            ),
        ]

        failure_reason = None
        feasible = True
        for passed, reason in checks:
            if not passed:
                feasible = False
                failure_reason = reason
                break

        repaired = None
        repair_available = False
        safety_score = 1.0

        if not feasible:
            repaired = repair_action(action, failure_reason)
            repair_available = repaired is not None
            safety_score = 0.5 if repair_available else 0.0

        latency_ms = (time.perf_counter() - start) * 1000.0

        return FeasibilityVerdict(
            action_id=action_id,
            action_type=action_type,
            feasible=feasible,
            failure_reason=failure_reason,
            repair_available=repair_available,
            repaired_action=repaired,
            safety_score=safety_score,
            latency_ms=round(latency_ms, 3),
        )

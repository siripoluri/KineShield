import time
from typing import Any, Dict, Optional

from kineshield.feasibility.collision_checker import check_collision_risk
from kineshield.feasibility.ik_checker import check_ik_reachability
from kineshield.feasibility.timing_checker import check_timing_feasibility
from kineshield.feasibility.workspace_checker import check_workspace_bounds
from kineshield.repair.repair_policy import repair_action
from kineshield.verdict.verdict_schema import FeasibilityVerdict


class FeasibilityChecker:
    """Baseline feasibility checker for structured robot actions.

    By default, this class uses a lightweight IK proxy so the repo can run
    without ROS/MoveIt. For real MoveIt integration, pass a MoveItIKChecker
    instance through `ik_backend`.
    """

    def __init__(
        self,
        max_reach_m: float = 1.2,
        workspace_bounds=((-1.0, 1.0), (-1.0, 1.0), (0.0, 1.2)),
        ik_backend: Optional[Any] = None,
    ) -> None:
        self.max_reach_m = max_reach_m
        self.workspace_bounds = workspace_bounds
        self.ik_backend = ik_backend

    def check(self, action: Dict[str, Any]) -> FeasibilityVerdict:
        start = time.perf_counter()

        action_id = str(action.get("action_id", "unknown"))
        action_type = str(action.get("action_type", "unknown"))

        target_pose = action.get("target_pose", {})
        position = target_pose.get("position", action.get("target_position", [0.0, 0.0, 0.0]))
        orientation = target_pose.get("orientation", [0.0, 0.0, 0.0, 1.0])
        constraints = action.get("constraints", {})

        failure_reason = self._run_checks(
            action=action,
            position=position,
            orientation=orientation,
            constraints=constraints,
        )

        feasible = failure_reason is None
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

    def _run_checks(
        self,
        action: Dict[str, Any],
        position,
        orientation,
        constraints: Dict[str, Any],
    ) -> Optional[str]:
        workspace_ok, workspace_reason = check_workspace_bounds(position, self.workspace_bounds)
        if not workspace_ok:
            return workspace_reason

        ik_ok, ik_reason = self._check_ik(position, orientation)
        if not ik_ok:
            return ik_reason

        collision_ok, collision_reason = check_collision_risk(action)
        if not collision_ok:
            return collision_reason

        timing_ok, timing_reason = check_timing_feasibility(
            float(action.get("estimated_duration_s", 1.0)),
            float(constraints.get("max_duration_s", 3.0)),
        )
        if not timing_ok:
            return timing_reason

        return None

    def _check_ik(self, position, orientation) -> tuple[bool, Optional[str]]:
        """Use MoveIt IK backend when available; otherwise use fallback proxy."""
        if self.ik_backend is not None:
            result = self.ik_backend.check_pose(position, orientation)
            return result.reachable, result.failure_reason

        return check_ik_reachability(position, self.max_reach_m)
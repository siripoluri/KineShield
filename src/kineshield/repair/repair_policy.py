from copy import deepcopy
from typing import Any, Dict, Optional


def repair_action(action: Dict[str, Any], failure_reason: Optional[str]) -> Optional[Dict[str, Any]]:
    """Return a conservative repaired action when possible.

    This baseline repair policy is intentionally simple. It demonstrates the
    interface used by KineShield before replacing it with robot-specific repair
    logic.
    """
    if failure_reason is None:
        return None

    repaired = deepcopy(action)
    target_pose = repaired.setdefault("target_pose", {})
    position = target_pose.get("position", repaired.get("target_position"))

    if failure_reason.startswith("workspace_violation") and isinstance(position, list) and len(position) == 3:
        target_pose["position"] = [
            max(-1.0, min(1.0, float(position[0]))),
            max(-1.0, min(1.0, float(position[1]))),
            max(0.0, min(1.2, float(position[2]))),
        ]
        repaired["repair_note"] = "clamped_target_pose_to_workspace"
        return repaired

    if failure_reason == "ik_unreachable" and isinstance(position, list) and len(position) == 3:
        target_pose["position"] = [0.75, 0.0, 0.45]
        repaired["repair_note"] = "moved_target_to_nominal_reachable_pose"
        return repaired

    if failure_reason == "timing_infeasible":
        repaired.setdefault("constraints", {})["max_duration_s"] = float(
            repaired.get("estimated_duration_s", 1.0)
        ) + 0.5
        repaired["repair_note"] = "expanded_time_budget"
        return repaired

    return None

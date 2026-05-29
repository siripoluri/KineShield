from math import sqrt
from typing import Optional, Sequence


def check_ik_reachability(
    target_position: Sequence[float],
    max_reach_m: float,
) -> tuple[bool, Optional[str]]:
    """Baseline IK reachability proxy.

    This fallback is used when MoveIt is not available. It gives the repo a
    lightweight non-ROS path for tests and examples.
    """
    if len(target_position) != 3:
        return False, "invalid_target_pose"

    distance = sqrt(sum(float(v) ** 2 for v in target_position))
    if distance > max_reach_m:
        return False, "ik_unreachable"

    return True, None
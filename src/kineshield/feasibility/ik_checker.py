from math import sqrt
from typing import Optional, Sequence


def check_ik_reachability(
    target_position: Sequence[float],
    max_reach_m: float,
) -> tuple[bool, Optional[str]]:
    """Baseline IK reachability proxy.

    This is a scaffold for early testing. A full version can replace this with
    a MoveIt IK service call or robot-specific kinematics solver.
    """
    if len(target_position) != 3:
        return False, "invalid_target_pose"

    distance = sqrt(sum(float(v) ** 2 for v in target_position))
    if distance > max_reach_m:
        return False, "ik_unreachable"

    return True, None

from typing import Dict, Optional, Tuple


def check_joint_limits(
    joint_values: Dict[str, float],
    joint_limits: Dict[str, Tuple[float, float]],
) -> tuple[bool, Optional[str]]:
    """Return whether all joints are within configured limits."""
    for joint, value in joint_values.items():
        if joint not in joint_limits:
            return False, f"missing_joint_limit:{joint}"

        lower, upper = joint_limits[joint]
        if value < lower or value > upper:
            return False, f"joint_limit_violation:{joint}"

    return True, None

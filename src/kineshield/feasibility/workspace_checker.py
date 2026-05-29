from typing import Optional, Sequence, Tuple


def check_workspace_bounds(
    position: Sequence[float],
    bounds: Tuple[Tuple[float, float], Tuple[float, float], Tuple[float, float]],
) -> tuple[bool, Optional[str]]:
    """Check whether an xyz position falls within workspace bounds."""
    if len(position) != 3:
        return False, "invalid_position"

    for axis, value in zip(("x", "y", "z"), position):
        lower, upper = bounds[("x", "y", "z").index(axis)]
        if value < lower or value > upper:
            return False, f"workspace_violation:{axis}"

    return True, None

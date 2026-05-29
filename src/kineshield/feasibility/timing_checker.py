from typing import Optional


def check_timing_feasibility(
    estimated_duration_s: float,
    max_duration_s: float,
) -> tuple[bool, Optional[str]]:
    """Check whether an action can finish within the requested time budget."""
    if estimated_duration_s < 0:
        return False, "invalid_duration"

    if estimated_duration_s > max_duration_s:
        return False, "timing_infeasible"

    return True, None

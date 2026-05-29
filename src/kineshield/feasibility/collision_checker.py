from typing import Any, Dict, Optional


def check_collision_risk(action: Dict[str, Any]) -> tuple[bool, Optional[str]]:
    """Placeholder collision check.

    In the full system, this should connect to a planning scene through MoveIt
    or another collision-checking backend.
    """
    constraints = action.get("constraints", {})
    if constraints.get("mock_collision", False):
        return False, "collision_risk"

    return True, None

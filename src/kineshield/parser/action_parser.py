from typing import Any, Dict


REQUIRED_FIELDS = {"action_id", "action_type"}


def parse_action(raw_action: Dict[str, Any]) -> Dict[str, Any]:
    missing = REQUIRED_FIELDS - set(raw_action.keys())
    if missing:
        raise ValueError(f"invalid_action_schema: missing {sorted(missing)}")

    action = dict(raw_action)
    action.setdefault("constraints", {})
    return action

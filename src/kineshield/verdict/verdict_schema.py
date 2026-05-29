from dataclasses import asdict, dataclass
from typing import Any, Dict, Optional


@dataclass
class FeasibilityVerdict:
    """Structured result returned by KineShield after checking an action."""

    action_id: str
    action_type: str
    feasible: bool
    failure_reason: Optional[str]
    repair_available: bool
    repaired_action: Optional[Dict[str, Any]]
    safety_score: float
    latency_ms: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

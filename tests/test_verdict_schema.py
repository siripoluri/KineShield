from kineshield.verdict.verdict_schema import FeasibilityVerdict


def test_verdict_to_dict() -> None:
    verdict = FeasibilityVerdict(
        action_id="test_001",
        action_type="move_end_effector",
        feasible=False,
        failure_reason="joint_limit_violation",
        repair_available=True,
        repaired_action={"action_type": "move_end_effector"},
        safety_score=0.8,
        latency_ms=12.5,
    )

    data = verdict.to_dict()

    assert data["action_id"] == "test_001"
    assert data["feasible"] is False
    assert data["repair_available"] is True
    assert data["latency_ms"] == 12.5

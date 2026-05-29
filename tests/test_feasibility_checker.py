from kineshield.feasibility.feasibility_checker import FeasibilityChecker


def test_reachable_action_is_feasible() -> None:
    checker = FeasibilityChecker()
    action = {
        "action_id": "reach_001",
        "action_type": "move_end_effector",
        "target_pose": {"position": [0.4, 0.1, 0.3]},
        "estimated_duration_s": 1.0,
        "constraints": {"max_duration_s": 2.0},
    }

    verdict = checker.check(action)

    assert verdict.feasible is True
    assert verdict.failure_reason is None


def test_unreachable_action_returns_repair() -> None:
    checker = FeasibilityChecker()
    action = {
        "action_id": "reach_002",
        "action_type": "move_end_effector",
        "target_pose": {"position": [3.2, 0.1, 1.8]},
        "estimated_duration_s": 1.0,
        "constraints": {"max_duration_s": 2.0},
    }

    verdict = checker.check(action)

    assert verdict.feasible is False
    assert verdict.failure_reason is not None
    assert verdict.repair_available is True

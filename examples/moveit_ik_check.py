import json
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

try:
    import rclpy
except ImportError as exc:
    raise SystemExit(
        "This example requires ROS 2. Source your ROS 2 workspace first, then retry."
    ) from exc

from kineshield.feasibility.feasibility_checker import FeasibilityChecker
from kineshield.feasibility.moveit_ik_checker import MoveItIKChecker
from kineshield.parser.action_parser import parse_action


def main() -> None:
    rclpy.init()

    ik_backend = None

    try:
        ik_backend = MoveItIKChecker(
            group_name="manipulator",
            end_effector_link="tool0",
            frame_id="base_link",
            service_name="/compute_ik",
            timeout_sec=2.0,
        )

        checker = FeasibilityChecker(ik_backend=ik_backend)

        action = parse_action(
            {
                "action_id": "moveit_reach_001",
                "action_type": "move_end_effector",
                "target_pose": {
                    "position": [0.45, 0.10, 0.35],
                    "orientation": [0.0, 0.0, 0.0, 1.0],
                },
                "estimated_duration_s": 1.5,
                "constraints": {
                    "max_duration_s": 2.0,
                    "avoid_collisions": True,
                },
            }
        )

        verdict = checker.check(action)
        print(json.dumps(verdict.to_dict(), indent=2))

    finally:
        if ik_backend is not None:
            ik_backend.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
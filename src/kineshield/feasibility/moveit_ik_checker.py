from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

try:
    import rclpy
    from geometry_msgs.msg import PoseStamped
    from moveit_msgs.msg import MoveItErrorCodes
    from moveit_msgs.srv import GetPositionIK
    from rclpy.node import Node
except ImportError:  # Allows repo tests to run without ROS/MoveIt installed.
    rclpy = None
    PoseStamped = None
    MoveItErrorCodes = None
    GetPositionIK = None
    Node = object


@dataclass
class IKResult:
    reachable: bool
    failure_reason: Optional[str]
    latency_ms: Optional[float] = None


class MoveItIKChecker(Node):
    """MoveIt-based IK checker for KineShield.

    This class calls MoveIt's `/compute_ik` service to validate whether a
    target end-effector pose is reachable for the configured planning group.

    Requirements:
    - ROS 2 environment sourced
    - MoveIt 2 installed
    - move_group running
    - `/compute_ik` service available
    """

    def __init__(
        self,
        group_name: str = "manipulator",
        end_effector_link: str = "tool0",
        frame_id: str = "base_link",
        service_name: str = "/compute_ik",
        timeout_sec: float = 2.0,
    ) -> None:
        if rclpy is None:
            raise ImportError(
                "ROS 2 / MoveIt dependencies are not installed. "
                "Install rclpy, geometry_msgs, and moveit_msgs in a ROS 2 environment."
            )

        super().__init__("kineshield_moveit_ik_checker")

        self.group_name = group_name
        self.end_effector_link = end_effector_link
        self.frame_id = frame_id
        self.timeout_sec = timeout_sec

        self.client = self.create_client(GetPositionIK, service_name)

        if not self.client.wait_for_service(timeout_sec=timeout_sec):
            raise RuntimeError(
                f"MoveIt IK service '{service_name}' is not available. "
                "Make sure move_group is running."
            )

    def check_pose(
        self,
        position: Sequence[float],
        orientation: Sequence[float] | None = None,
    ) -> IKResult:
        """Check whether a target pose is IK-reachable.

        Args:
            position: xyz target position.
            orientation: quaternion xyzw. Defaults to identity orientation.

        Returns:
            IKResult describing reachability and failure reason.
        """
        if len(position) != 3:
            return IKResult(False, "invalid_target_position")

        if orientation is None:
            orientation = [0.0, 0.0, 0.0, 1.0]

        if len(orientation) != 4:
            return IKResult(False, "invalid_target_orientation")

        request = GetPositionIK.Request()
        request.ik_request.group_name = self.group_name
        request.ik_request.ik_link_name = self.end_effector_link
        request.ik_request.timeout.sec = int(self.timeout_sec)
        request.ik_request.avoid_collisions = True

        pose = PoseStamped()
        pose.header.frame_id = self.frame_id
        pose.pose.position.x = float(position[0])
        pose.pose.position.y = float(position[1])
        pose.pose.position.z = float(position[2])
        pose.pose.orientation.x = float(orientation[0])
        pose.pose.orientation.y = float(orientation[1])
        pose.pose.orientation.z = float(orientation[2])
        pose.pose.orientation.w = float(orientation[3])

        request.ik_request.pose_stamped = pose

        start = self.get_clock().now()
        future = self.client.call_async(request)
        rclpy.spin_until_future_complete(self, future, timeout_sec=self.timeout_sec)

        end = self.get_clock().now()
        latency_ms = (end - start).nanoseconds / 1_000_000.0

        if not future.done() or future.result() is None:
            return IKResult(False, "ik_service_timeout", latency_ms)

        response = future.result()
        error_code = response.error_code.val

        if error_code == MoveItErrorCodes.SUCCESS:
            return IKResult(True, None, latency_ms)

        return IKResult(False, self._map_moveit_error(error_code), latency_ms)

    @staticmethod
    def _map_moveit_error(error_code: int) -> str:
        error_map = {
            MoveItErrorCodes.FAILURE: "ik_failure",
            MoveItErrorCodes.PLANNING_FAILED: "ik_planning_failed",
            MoveItErrorCodes.INVALID_MOTION_PLAN: "invalid_motion_plan",
            MoveItErrorCodes.MOTION_PLAN_INVALIDATED_BY_ENVIRONMENT_CHANGE: "environment_changed",
            MoveItErrorCodes.CONTROL_FAILED: "control_failed",
            MoveItErrorCodes.UNABLE_TO_AQUIRE_SENSOR_DATA: "sensor_data_unavailable",
            MoveItErrorCodes.TIMED_OUT: "ik_service_timeout",
            MoveItErrorCodes.PREEMPTED: "ik_preempted",
            MoveItErrorCodes.START_STATE_IN_COLLISION: "start_state_in_collision",
            MoveItErrorCodes.START_STATE_VIOLATES_PATH_CONSTRAINTS: "start_state_violates_constraints",
            MoveItErrorCodes.GOAL_IN_COLLISION: "goal_in_collision",
            MoveItErrorCodes.GOAL_VIOLATES_PATH_CONSTRAINTS: "goal_violates_constraints",
            MoveItErrorCodes.GOAL_CONSTRAINTS_VIOLATED: "goal_constraints_violated",
            MoveItErrorCodes.INVALID_GROUP_NAME: "invalid_group_name",
            MoveItErrorCodes.INVALID_GOAL_CONSTRAINTS: "invalid_goal_constraints",
            MoveItErrorCodes.INVALID_ROBOT_STATE: "invalid_robot_state",
            MoveItErrorCodes.INVALID_LINK_NAME: "invalid_link_name",
            MoveItErrorCodes.INVALID_OBJECT_NAME: "invalid_object_name",
            MoveItErrorCodes.FRAME_TRANSFORM_FAILURE: "frame_transform_failure",
            MoveItErrorCodes.COLLISION_CHECKING_UNAVAILABLE: "collision_checking_unavailable",
            MoveItErrorCodes.ROBOT_STATE_STALE: "robot_state_stale",
            MoveItErrorCodes.SENSOR_INFO_STALE: "sensor_info_stale",
            MoveItErrorCodes.NO_IK_SOLUTION: "ik_unreachable",
        }

        return error_map.get(error_code, f"moveit_error:{error_code}")
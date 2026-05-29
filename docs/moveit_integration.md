# MoveIt IK Integration

KineShield includes an optional MoveIt-based IK checker that replaces the lightweight distance-based IK proxy with a real `/compute_ik` service call.

## Requirements

- ROS 2
- MoveIt 2
- A robot description loaded into MoveIt
- `move_group` running
- `/compute_ik` service available

## Run

Source ROS 2 and your MoveIt workspace:

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
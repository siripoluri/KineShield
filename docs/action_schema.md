# Action Schema

KineShield expects VLM/VLA-generated actions to be converted into a structured action object before feasibility checking.

## Example Action

```json
{
  "action_id": "reach_001",
  "action_type": "move_end_effector",
  "target_pose": {
    "position": [0.45, 0.12, 0.30],
    "orientation": [0.0, 0.0, 0.0, 1.0]
  },
  "constraints": {
    "max_duration_s": 2.0,
    "avoid_collisions": true
  }
}
```

## Required Fields

- `action_id`: unique action identifier
- `action_type`: action category
- `target_pose`: desired robot pose or target
- `constraints`: optional execution constraints

## Supported Failure Reasons

- `ik_unreachable`
- `joint_limit_violation`
- `collision_risk`
- `workspace_violation`
- `timing_infeasible`
- `invalid_action_schema`

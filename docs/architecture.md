# Architecture

KineShield is designed as a deterministic safety layer between a VLM/VLA planner and a robot execution stack.

## Pipeline

1. Action proposal from VLM/VLA
2. Action parsing into a structured schema
3. Feasibility checks:
   - IK reachability
   - Collision status
   - Joint limits
   - Workspace bounds
   - Timing feasibility
4. Repair attempt if infeasible
5. Structured verdict returned to planner/controller

## Design Goal

The goal is not to replace learning-based planners. The goal is to prevent physically infeasible actions from reaching execution and to provide structured explanations when a proposed action fails.

## Deployment Split

- **Jetson / edge node:** lightweight feasibility checks, structured verdict generation, latency logging
- **Workstation / development environment:** full simulation validation, Gazebo/MoveIt experiments, benchmark sweeps

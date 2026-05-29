# KineShield

KineShield is a real-time feasibility firewall for vision-language robot actions. It checks whether a proposed robot action is physically executable before the action reaches a robot controller.

The system validates actions using deterministic constraints such as inverse kinematics, collision checking, joint limits, workspace bounds, and timing feasibility. If an action is infeasible, KineShield returns a structured failure reason and repairs the action to the closest feasible alternative when possible.

## Why This Matters

Vision-language models can generate actions that are semantically plausible but physically impossible. KineShield focuses on detecting and repairing these **kinematic hallucinations** before execution, helping make VLM/VLA-based robotics systems safer, more interpretable, and easier to debug.

## Core Features

* Feasibility checks for VLM-generated robot actions
* IK, collision, joint-limit, workspace, and timing validation
* Structured failure reasons for debugging and evaluation
* Repair logic for closest feasible alternatives
* KineHalluBench benchmark for measuring kinematic hallucinations
* Jetson-focused latency tracking for edge deployment

## System Architecture

```text
VLM Action Proposal
        ↓
Action Parser
        ↓
Feasibility Checker
        ↓
Repair Module
        ↓
Safety Verdict
        ↓
Robot Execution / Rejection
```

## Example Output

```json
{
  "action": "move gripper to target_pose",
  "feasible": false,
  "failure_reason": "joint_limit_violation",
  "violated_joint": "elbow_joint",
  "repair_available": true,
  "repaired_action": "move gripper to nearest reachable pose",
  "safety_score": 0.82,
  "latency_ms": 14.6
}
```

## KineHalluBench

KineHalluBench is the benchmark component of KineShield. It is designed to evaluate how often VLM-generated robot actions contain kinematic hallucinations and how effectively a safety layer can detect, reject, or repair them.

### Metrics

* Kinematic hallucination rate
* Shield acceptance / rejection accuracy
* Repair success rate
* Failure reason correctness
* Safety outcome improvement
* Jetson feasibility-check latency

## Jetson Deployment Target

KineShield is designed with Jetson-targeted edge deployment in mind. Lightweight feasibility checks and structured verdict generation are intended to run on-device, while heavier simulation validation and full benchmark evaluation can be run off-board during development.

## Project Status

KineShield is currently under active development. The repository includes the initial architecture, action schema, feasibility verdict format, and benchmark design, with MoveIt/Gazebo validation and Jetson latency benchmarking in progress.

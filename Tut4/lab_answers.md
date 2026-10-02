# Logical Planning — Lab Answers

## Task 0 — Initial State, Goal and Actions

### Starting configuration

The planner begins with the following facts:

```text
{At(Robot,A), At(Package,A)}
```

This means that both the robot and the package are initially located at `A`.

### Desired state

The planning process is successful when the package reaches location `C`:

```text
{At(Package,C)}
```

### Available actions

The action set includes movement, pickup and drop operations:

```text
Move(A,B)
Move(B,A)
Move(B,C)
Move(C,B)

PickUp(Package,A/B/C)
Drop(Package,A/B/C)
```

Each operation has its own logical preconditions and effects.

### Actions possible at the beginning

`PickUp(Package,A)` can be executed immediately because the initial state contains both:

```text
At(Robot,A)
At(Package,A)
```

On the other hand, `Drop(Package,C)` cannot currently be performed. It requires the robot to be at `C` while carrying the package, neither of which is true in the initial state.

---

# Task 1 — Constructing a Valid Plan

One valid solution is:

```text
PickUp(Package,A)
Move(A,B)
Move(B,C)
Drop(Package,C)
```

The sequence works because the package is picked up before the robot starts carrying it toward the destination.

The resulting state progression is:

```text
Initial
  |
  | PickUp(Package,A)
  v
Robot at A, Holding Package
  |
  | Move(A,B)
  v
Robot at B, Holding Package
  |
  | Move(B,C)
  v
Robot at C, Holding Package
  |
  | Drop(Package,C)
  v
Package at C
```

A move-first solution can also be valid. The important requirement is not the exact ordering of actions, but whether the preconditions of **every individual action** are satisfied when that action is executed.

---

# Task 4 — Planning Process

The planner can be understood as repeatedly performing the following operations:

```text
             Current state
                   |
                   v
          Examine available actions
                   |
                   v
        Check their preconditions
                   |
                   v
          Generate valid actions
                   |
                   v
        Produce successor states
                   |
                   v
          Search possible states
                   |
                   v
              Goal reached?
```

The logical component determines which actions are legal from a particular state.

The search component then explores the different legal action sequences until a state satisfying the goal is discovered.

---

# Task 5 — Checking State Transitions

The state transitions produced by the actual implementation provide a direct way of checking whether the planner is behaving correctly.

For example, after executing:

```text
PickUp(Package,A)
```

the state should indicate that the robot is carrying the package rather than treating the package as still being independently located at `A`.

Similarly, after:

```text
Drop(Package,C)
```

the final state should contain:

```text
At(Package,C)
```

Checking the actual transitions is therefore useful for validating that the action definitions and state-update mechanism agree with the planning specification.

---

# Reflection

## 1. Why define preconditions and effects?

Preconditions specify exactly when an action is allowed to execute, while effects describe the changes that occur afterward.

Together, they provide a precise description of the planning environment and prevent ambiguous action behaviour.

---

## 2. What could go wrong without precondition checking?

The planner could generate physically or logically impossible actions.

For example, it might attempt:

```text
Drop(Package,C)
```

while the robot is still at `A`, or while the robot is not carrying the package.

Such an action would produce an invalid plan.

---

## 3. Why can a plausible-looking plan still be invalid?

A sequence of actions is only a valid plan if every action can actually be executed in the state immediately before it.

An action that looks reasonable in isolation may become invalid because an earlier action changed the state.

---

## 4. What must be checked in a generated plan?

The following should be verified:

* Preconditions of every action.
* Effects of every action.
* State after each transition.
* Final goal condition.
* Behaviour when no valid plan exists.

---

## 5. Where does logical reasoning occur?

Logical reasoning occurs when the planner checks whether an action's preconditions are satisfied by the current state.

Formally:

```text
S |= Preconditions(a)
```

If this condition holds, action `a` can be used to generate a new state.

---

## 6. How does planning become a search problem?

Starting from the initial state, every applicable action creates a possible successor state.

The planner therefore explores a state-space tree:

```text
Initial state
     |
  Actions
   /   \
State  State
  |      |
Actions Actions
  |      |
 ...    ...
     \  /
    Goal
```

Breadth-First Search is used to explore these possibilities in the implementation.

Thus, planning combines **logical action applicability** with **state-space search** to find a sequence that reaches the required goal.

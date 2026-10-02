# Logical Planning Agent

This repository contains an implementation for the **Artificial Intelligence Laboratory – Logical Planning** exercise.

The laboratory models planning using three main components:

```text
Initial State + Actions + Goal
```

Each action describes the conditions under which it can be executed and the changes it makes to the current state. Planning then becomes a search through the possible sequences of valid actions.

---

## Warehouse Planning Problem

The environment contains three locations:

```text
A, B, C
```

The initial configuration is:

```text
At(Robot, A)
At(Package, A)
```

The required goal is:

```text
At(Package, C)
```

The available actions describe how the robot can move, pick up the package, and release it at another location. Every action has a set of preconditions and effects that determine when it can be executed and how it modifies the state.

---

## Example Plan

One valid sequence of actions is:

```text
Move(A, B)
PickUp(Package, B)
Move(B, C)
Drop(Package, C)
```

The important requirement is that every action must be valid in the state produced by the previous action.

The resulting states are:

```text
S0:
At(Robot, A)
At(Package, A)

S1:
At(Robot, B)
At(Package, A)

S2:
At(Robot, B)
Holding(Package)

S3:
At(Robot, C)
Holding(Package)

S4:
At(Robot, C)
At(Package, C)
```

The final state satisfies the required goal because the package is located at `C`.

---

## Action Representation

Each action is represented using four sets of logical conditions:

```text
positive_preconditions
negative_preconditions
positive_effects
negative_effects
```

Before an action is executed, its preconditions are checked against the current state.

If the action is applicable, the state is updated by removing facts listed in its negative effects and adding facts listed in its positive effects.

Conceptually:

```text
Current state
      |
      v
Check preconditions
      |
      v
Action applicable?
      |
     Yes
      |
      v
Remove negative effects
      |
      v
Add positive effects
      |
      v
New state
```

---

## Planning Algorithm

Breadth-First Search is used to explore possible action sequences.

Starting from the initial state, the planner:

1. Checks which actions are currently applicable.
2. Applies each valid action to generate successor states.
3. Adds previously unseen states to the search queue.
4. Checks each state against the goal condition.
5. Reconstructs the sequence of actions once a goal state is reached.

Because the planner searches through states rather than blindly executing actions, it can determine a valid sequence automatically.

Run the planner with:

```bash
python planner.py
```

---

# Testing

The implementation is tested using several different planning scenarios.

## Test A — Solvable Problem

The original warehouse problem is used without modification.

Expected result:

```text
A valid plan is found.
The resulting state satisfies At(Package, C).
```

This verifies the normal planning behaviour.

---

## Test B — No Pickup Action

The pickup operation is removed from the available action set.

Since the robot can no longer obtain the package, it should be impossible to move the package to the destination.

Expected result:

```text
No plan found.
```

This also verifies that the planner only uses actions that are actually available.

---

## Test C — Irrelevant Movement

An additional action is introduced that can move the robot but does not change the package's location.

The planner should still evaluate the actual goal:

```text
At(Package, C)
```

rather than incorrectly treating:

```text
At(Robot, C)
```

as a successful solution.

Run all tests using:

```bash
python tests.py
```

---

## Logic and Search

Two separate ideas are involved in the planner.

### Logical reasoning

Before an action can be used, its preconditions must hold in the current state:

```text
S |= Preconditions(action)
```

If the condition is satisfied, the action can produce a successor state.

### Search

Once the applicable actions have been identified, the search algorithm determines which possible action sequences should be explored.

A useful way to summarize the relationship is:

```text
Logic → determines which actions are valid
Search → determines which valid actions to explore
```

The two components therefore work together to produce a valid plan.

---

# Reflection

### Why are preconditions and effects important?

They provide an exact description of when an action is allowed and what changes after the action occurs. This prevents the planner from performing operations that are inconsistent with the current state.

### What could happen if preconditions were ignored?

The planner could generate invalid sequences. For example, it might attempt to pick up the package when the robot is not at the package's location, or attempt to drop a package that is not currently being carried.

### Why isn't a plausible sequence necessarily a valid plan?

Every action must be applicable **at the exact point where it occurs in the sequence**. An action that is valid initially may become invalid after earlier actions change the state.

### How is logical reasoning used?

Logical conditions determine whether an action can be executed from the current state.

### How does planning become a search problem?

Each applicable action produces a possible successor state. The planner searches through these states until it finds one satisfying the goal condition.

---

## Project Files

```text
planner.py
tests.py
lab_answers.md
README.md
.gitignore
```

The implementation demonstrates how explicit action rules can be combined with state-space search to solve a small logical planning problem.

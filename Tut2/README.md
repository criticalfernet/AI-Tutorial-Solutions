# Goal-Based Warehouse Navigation Agent

This project implements a simple goal-directed agent for navigating a warehouse represented as a two-dimensional grid. It was developed as part of the **Agents: Laboratory Exercise – Constructing a Goal-Based Agent using a Large Language Model**.

The vehicle is given a starting location and a destination and must determine a route to the destination without entering blocked cells. An LLM was also used during development as a programming assistant, followed by manual testing of the resulting implementation.

## Environment

The warehouse is represented using a grid containing four possible symbols:

| Symbol | Meaning                 |
| ------ | ----------------------- |
| `S`    | Starting location       |
| `G`    | Destination             |
| `#`    | Blocked cell / obstacle |
| `.`    | Traversable cell        |

The vehicle can move one cell at a time in any of the four cardinal directions:

```text
        Up
         ↑
Left ← Agent → Right
         ↓
       Down
```

A valid route must remain inside the grid and cannot pass through an obstacle.

## Agent Design

The implementation uses **Breadth-First Search (BFS)** to find the route.

BFS is appropriate here because every movement between adjacent cells has the same cost. It explores the grid level by level, so once the goal is reached, the resulting route contains the minimum number of movements for this type of grid.

The search works roughly as follows:

```text
Locate S and G
     ↓
Insert S into the search queue
     ↓
Take the next position
     ↓
Check its four neighbours
     ↓
Ignore invalid/blocked/already visited cells
     ↓
Record valid cells and their parent
     ↓
Continue until G is found
     ↓
Follow parent links back to S
     ↓
Reverse the resulting path
```

For every discovered position, the program records where it came from. This allows the final route to be reconstructed after the search reaches the destination.

## Why This Qualifies as a Goal-Based Agent

The agent's behaviour is determined by an explicitly defined destination.

Instead of simply choosing an action based on the current cell, it searches through possible future states and constructs a sequence of actions that leads from the starting state to the specified goal.

The search therefore involves:

* A representation of the current state
* A set of possible actions
* Knowledge of previously visited states
* A specified goal state
* A sequence of actions leading to that goal

## Task 1

### 1. What is the environment?

The environment is a two-dimensional warehouse grid containing traversable locations and blocked locations representing obstacles.

### 2. What is the goal?

The objective is to move the vehicle from the cell marked `S` to the cell marked `G`.

### 3. What actions can the agent perform?

The available actions are:

* Up
* Down
* Left
* Right

Each action attempts to move the vehicle by one grid cell.

### 4. What information does the agent need to maintain?

During the search, the agent keeps track of its position and the locations that have already been explored. Parent information is also stored so that the discovered route can be reconstructed once the goal is reached.

### 5. Why is this a goal-based agent?

The agent is explicitly given a destination and evaluates possible future states in order to produce a sequence of actions that achieves that destination.

## Testing

The implementation can be executed with:

```bash
python warehouse_agent.py
```

The accompanying tests can be run using:

```bash
python tests.py
```

The test cases cover multiple situations, including:

1. The warehouse configuration provided by the laboratory.
2. A simple case where the destination is only a short distance from the start.
3. A configuration in which the destination cannot be reached.

Testing the impossible case is particularly useful because the search should terminate without incorrectly claiming that a route exists.

The generated code was subsequently executed against the supplied environment and test cases. The LLM output was therefore used as a development aid, while the correctness of the implementation was checked through actual execution.

## Project Structure

```text
warehouse_agent.py   # Agent and BFS implementation
tests.py             # Test cases
README.md            # Project documentation
lab_answers.md       # Lab Answers
.gitignore
```

The implementation intentionally uses a simple search algorithm so that the agent's state representation, goal, available actions, and route-search process remain easy to inspect.

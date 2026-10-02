# Search Algorithms and A* — AI Laboratory

This project implements search-based navigation for a warehouse robot as part of the **Artificial Intelligence Laboratory – Search and A*** exercise.

The warehouse is represented as a grid, and the robot must determine a sequence of movements that takes it from its starting position to the specified destination. The project also compares uninformed search with A* and examines how different heuristic functions affect the search.

---

## 1. Warehouse Navigation

The robot operates on a grid containing free spaces and obstacles.

Four actions are available:

```text
Up
Down
Left
Right
```

Each movement has a cost of `1`.

The warehouse layout used by the program is the one specified in the laboratory exercise.

---

## 2. Problem Representation

The navigation task can be expressed as a standard search problem.

| Element     | Definition                                            |
| ----------- | ----------------------------------------------------- |
| State       | Robot's current `(row, column)` coordinates           |
| Actions     | Up, Down, Left, Right                                 |
| Successor   | Adjacent cell that is inside the grid and not blocked |
| Start state | Position marked `S`                                   |
| Goal state  | Position marked `G`                                   |
| Step cost   | `1`                                                   |

Since the warehouse does not contain randomness, executing the same action from the same state always produces the same resulting state. The problem is therefore deterministic.

---

## 3. A* Search

The main search algorithm is A*.

For a node `n`, A* evaluates:

```text
f(n) = g(n) + h(n)
```

where:

* `g(n)` represents the cost accumulated from the starting position.
* `h(n)` estimates the remaining cost to the goal.
* `f(n)` is the priority used when selecting the next state to explore.

The implementation maintains a priority queue containing the search frontier. It also records the best known `g` value for each position and stores parent information for reconstructing the final route.

The program reports:

* Whether a route was found
* Length/cost of the resulting route
* Number of states expanded during the search

Run the program with:

```bash
python search_agent.py
```

---

## 4. Test Cases

The accompanying tests check several different environments:

1. The original warehouse configuration.
2. A simple case where the goal is directly reachable.
3. A warehouse in which the goal cannot be reached.
4. An alternative-route configuration for checking path selection.

The tests also verify that the returned solution has the expected shortest-path behaviour where applicable.

Execute the tests using:

```bash
python tests.py
```

---

## 5. BFS as a Baseline

Breadth-First Search is included as a comparison with A*.

Because every movement has the same cost, BFS is capable of finding a minimum-cost route in this environment. However, it does not use information about where the goal is located when deciding which state to expand.

The program runs the search methods on the same warehouse and reports their results using:

```text
Solution found
Path length
Number of states expanded
```

This provides a direct way to observe the effect of using a heuristic to guide the search.

In cases where the heuristic provides useful directional information, A* may avoid expanding some states that BFS would otherwise explore.

---

## 6. Heuristic Experiments

The implementation evaluates A* using several different heuristic functions:

```text
Manhattan distance
h(n) = 0
Euclidean distance
2 × Manhattan distance
```

For each version, the experiment records whether a solution was obtained, the resulting path length, and the number of states expanded.

### Manhattan Distance

For a grid where diagonal movement is not permitted, Manhattan distance is a natural estimate:

```text
|row - goal_row| + |column - goal_column|
```

It represents the number of horizontal and vertical movements required if there were no obstacles in the way.

### Zero Heuristic

Setting:

```text
h(n) = 0
```

removes the heuristic contribution from A*. This provides a useful baseline because the search is then guided only by the accumulated cost `g(n)`.

### Euclidean Distance

The Euclidean heuristic measures straight-line distance between the current cell and the destination. It is another estimate of the remaining distance, although the robot itself is restricted to horizontal and vertical movements.

### Aggressive Heuristic

The experiment also includes:

```text
h(n) = 2 × Manhattan distance
```

This deliberately makes the heuristic more aggressive.

For A* to retain the standard optimality guarantee, the heuristic should not overestimate the actual remaining cost:

```text
h(n) ≤ h*(n)
```

Scaling Manhattan distance by two can violate this condition. The experiment therefore demonstrates why the properties of a heuristic matter and what can happen when the heuristic becomes too large.

---

The generated code was subsequently executed and checked against the supplied test scenarios rather than being assumed to be correct.

In particular, the original warehouse, simple reachable case, and impossible case were tested. Path lengths and termination behaviour were also inspected.

This is important because producing code that runs successfully does not by itself establish that the search algorithm is behaving correctly.

---

## 7. Project Files

```text
search_agent.py    # Search algorithms and heuristic experiments
tests.py           # Test cases
README.md          # Project documentation
lab_answers.md
.gitignore
```

The overall purpose of the project is to demonstrate how a warehouse navigation problem can be represented as a formal search problem, and then to compare uninformed search with heuristic-guided A* search.

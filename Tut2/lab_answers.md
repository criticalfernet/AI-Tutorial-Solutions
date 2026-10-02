# Lab Answers

## Task 1: Agent Description

**1. Environment**

The agent operates inside a 2-D warehouse represented as a grid. Some cells are available for movement, while others represent obstacles.

**2. Goal**

The vehicle must navigate from the starting cell `S` to the destination cell `G` without entering blocked cells.

**3. Available actions**

At each position, the vehicle can attempt one of four movements:

```text
Up
Down
Left
Right
```

**4. Information used during search**

The agent records the states it has already encountered along with parent relationships between states. This information allows it to avoid unnecessary revisits and reconstruct the route after finding the destination.

**5. Goal-based behaviour**

The important distinction is that the agent is working toward a known target state. It considers possible future states and searches for an action sequence that eventually reaches `G`, rather than simply reacting to the current cell.

### Additional Consideration

If the warehouse becomes significantly larger, BFS may consume considerable memory because it can have many grid positions in its queue and visited set. As the size of the state space increases, other search methods may become worth considering depending on the environment and requirements.

---

## Task 2: Agent Architecture

The overall flow of the agent can be represented as:

```text
             Warehouse
                 |
                 v
          Observe current state
                 |
                 v
       Generate possible moves
                 |
                 v
         Search for a route
                 |
                 v
          Check the goal
             /       \
          Found      Not found
            |            |
            v            |
       Build path <------+
            |
            v
       Execute route
```

The search component determines which states should be explored, while the goal test determines whether the required destination has been reached.

---

## Task 3: Testing

Three different situations were used to check the implementation:

* The original warehouse configuration from the laboratory.
* A very small case where the goal can be reached in a single movement.
* A map where no valid route exists.

For the original warehouse, the implementation found a route containing **20 movements**.

For the unreachable configuration, the search terminated correctly and reported that the destination could not be reached.

These cases check both successful path finding and failure handling.

---

## LLM-Based Development

### Was the generated program immediately accepted?

No assumptions were made about the generated implementation. The LLM-produced code was treated as an initial implementation and was subsequently executed against the test cases.

### How could the prompt be made more precise?

A useful prompt should clearly define:

* The format of the warehouse grid.
* The meaning of each grid symbol.
* Which movements are permitted.
* What constitutes a valid path.
* The required form of the output.
* Expected behaviour when no route exists.
* Any edge cases that should be tested.

Providing these constraints reduces ambiguity and makes the generated implementation easier to verify.

### Search method

The implementation uses **Breadth-First Search (BFS)**.

### Reason for choosing BFS

The warehouse is a small, unweighted grid in which every movement has the same cost. BFS explores positions according to their distance from the starting point, making it suitable for finding a route with the minimum number of moves in this setting.

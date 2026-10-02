import heapq
from collections import deque


MAP = [
    "#################",
    "#S....#.........#",
    "#.###.#.#######.#",
    "#...#.#.......#.#",
    "###.#.#######.#.#",
    "#...#.........#.#",
    "#.###########.#.#",
    "#.............#G#",
    "#################",
]


DIRECTIONS = (
    (-1, 0),   # up
    (1, 0),    # down
    (0, -1),   # left
    (0, 1),    # right
)


def locate(grid, marker):
    for row_number, row in enumerate(grid):
        column_number = row.find(marker)

        if column_number >= 0:
            return row_number, column_number

    raise ValueError(f"Grid does not contain {marker!r}")


def adjacent_cells(grid, position):
    row, column = position

    for row_delta, column_delta in DIRECTIONS:
        new_row = row + row_delta
        new_column = column + column_delta

        if not (
            0 <= new_row < len(grid)
            and 0 <= new_column < len(grid[new_row])
        ):
            continue

        if grid[new_row][new_column] == "#":
            continue

        yield new_row, new_column


def build_path(parents, destination):
    route = []
    current = destination

    while current is not None:
        route.append(current)
        current = parents[current]

    return list(reversed(route))


def h_manhattan(position, destination):
    return (
        abs(position[0] - destination[0])
        + abs(position[1] - destination[1])
    )


def h_euclidean(position, destination):
    row_difference = position[0] - destination[0]
    column_difference = position[1] - destination[1]

    return (
        row_difference ** 2
        + column_difference ** 2
    ) ** 0.5


def a_star(grid, heuristic=h_manhattan, scale=1.0):
    start = locate(grid, "S")
    goal = locate(grid, "G")

    # Entries are (priority, insertion_order, state).
    open_set = []
    sequence = 0

    heapq.heappush(open_set, (0, sequence, start))

    parents = {start: None}
    distance = {start: 0}

    expanded_count = 0

    while open_set:
        _, _, current = heapq.heappop(open_set)
        expanded_count += 1

        if current == goal:
            return build_path(parents, goal), expanded_count

        for neighbour in adjacent_cells(grid, current):
            candidate_cost = distance[current] + 1

            old_cost = distance.get(neighbour)

            if old_cost is not None and candidate_cost >= old_cost:
                continue

            distance[neighbour] = candidate_cost
            parents[neighbour] = current

            estimate = scale * heuristic(neighbour, goal)
            priority = candidate_cost + estimate

            sequence += 1
            heapq.heappush(
                open_set,
                (priority, sequence, neighbour)
            )

    return None, expanded_count


def breadth_first_search(grid):
    start = locate(grid, "S")
    goal = locate(grid, "G")

    queue = deque([start])
    parents = {start: None}

    expanded_count = 0

    while queue:
        current = queue.popleft()
        expanded_count += 1

        if current == goal:
            return build_path(parents, goal), expanded_count

        for neighbour in adjacent_cells(grid, current):
            if neighbour in parents:
                continue

            parents[neighbour] = current
            queue.append(neighbour)

    return None, expanded_count


def show_result(label, result):
    path, number_expanded = result

    print(label)
    print("-" * 40)

    if path is None:
        print("Solution found: No")
    else:
        print("Solution found: Yes")
        print("Path length:", len(path) - 1)
        print("Path:", path)

    print("States expanded:", number_expanded)
    print()


def main():
    print("Warehouse Search: BFS and A*")
    print("=" * 50)

    experiments = [
        ("BFS", lambda: breadth_first_search(MAP)),
        ("A* Manhattan", lambda: a_star(MAP)),
        ("A* h(n)=0", lambda: a_star(MAP, scale=0.0)),
        ("A* Euclidean", lambda: a_star(MAP, h_euclidean)),
        ("A* Manhattan x2", lambda: a_star(MAP, scale=2.0)),
    ]

    for title, experiment in experiments:
        show_result(title, experiment())


if __name__ == "__main__":
    main()

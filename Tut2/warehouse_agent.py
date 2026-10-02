from collections import deque


GRID = [
    "#####################",
    "#S....#............G#",
    "#.##....##########..#",
    "#....##.............#",
    "#.######.###.#.###..#",
    "#........#..........#",
    "#####################",
]


DIRECTIONS = [
    ("Up", -1, 0),
    ("Down", 1, 0),
    ("Left", 0, -1),
    ("Right", 0, 1),
]


def locate(grid, target):
    """Return the coordinates of the first occurrence of target."""
    for row_index, row in enumerate(grid):
        column_index = row.find(target)

        if column_index != -1:
            return row_index, column_index

    return None


def neighbours(grid, cell):
    """Generate all legal neighbouring cells."""
    row, column = cell

    for action, row_change, column_change in DIRECTIONS:
        next_row = row + row_change
        next_column = column + column_change

        inside_grid = (
            0 <= next_row < len(grid)
            and 0 <= next_column < len(grid[next_row])
        )

        if inside_grid and grid[next_row][next_column] != "#":
            yield action, (next_row, next_column)


def search(grid):
    start = locate(grid, "S")
    destination = locate(grid, "G")

    if start is None or destination is None:
        return None, {}

    frontier = deque([start])

    # Maps each discovered cell to the cell from which it was reached.
    previous = {start: None}

    # Stores the action used to enter each discovered cell.
    actions = {}

    while frontier:
        current = frontier.popleft()

        if current == destination:
            break

        for action, next_cell in neighbours(grid, current):
            if next_cell in previous:
                continue

            previous[next_cell] = current
            actions[next_cell] = action
            frontier.append(next_cell)

    if destination not in previous:
        return None, previous

    # Reconstruct the route by walking backwards from G.
    route = []
    cell = destination

    while cell != start:
        route.append(actions[cell])
        cell = previous[cell]

    route.reverse()

    return route, previous


def display_route(grid, route):
    current = locate(grid, "S")

    print("\nPath:")
    print(" -> ".join(route))
    print("Path length:", len(route))

    print("\nVisited positions in the final path:")
    print(current, end="")

    for action in route:
        for name, dr, dc in DIRECTIONS:
            if name == action:
                current = (
                    current[0] + dr,
                    current[1] + dc
                )
                break

        print(" ->", current, end="")

    print()


def run():
    route, discovered = search(GRID)

    print("Warehouse Navigation - Goal Based Agent")
    print("=" * 50)

    if route is None:
        print("No valid route exists.")
        return

    start = locate(GRID, "S")
    goal = locate(GRID, "G")

    print("Environment: warehouse grid")
    print("Start:", start)
    print("Goal:", goal)

    display_route(GRID, route)

    print("States discovered:", len(discovered))


if __name__ == "__main__":
    run()

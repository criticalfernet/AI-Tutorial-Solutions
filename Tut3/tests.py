from search_agent import a_star, h_manhattan


def evaluate_case(description, warehouse, expected_path, expected_steps=None):
    route, expanded = a_star(warehouse, h_manhattan)

    has_solution = route is not None
    passed = has_solution == expected_path

    if passed and expected_steps is not None:
        passed = len(route) - 1 == expected_steps

    result = "PASS" if passed else "FAIL"
    print(f"{description}: {result}")

    if has_solution:
        print(f"  path length: {len(route) - 1}")
        print(f"  states expanded: {expanded}")


def main():
    warehouse = [
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

    adjacent_goal = [
        "#####",
        "#SG.#",
        "#####",
    ]

    blocked_goal = [
        "#####",
        "#S#G#",
        "#####",
    ]

    cases = [
        ("Original warehouse", warehouse, True, None),
        ("Adjacent goal", adjacent_goal, True, 1),
        ("Blocked goal", blocked_goal, False, None),
    ]

    print("A* Search Tests")
    print("=" * 40)

    for title, grid, expected, length in cases:
        evaluate_case(
            title,
            grid,
            expected,
            length
        )


if __name__ == "__main__":
    main()

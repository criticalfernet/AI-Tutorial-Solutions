from warehouse_agent import search


def check_case(label, warehouse, should_have_path):
    result, discovered = search(warehouse)

    route_exists = result is not None
    passed = route_exists == should_have_path

    status = "PASS" if passed else "FAIL"
    print(f"{label:<22} {status}")

    if route_exists:
        print(f"  Number of moves: {len(result)}")
    else:
        print("  No route was returned.")


def main():
    test_cases = [
        (
            "Original warehouse",
            [
                "#####################",
                "#S....#............G#",
                "#.##....##########..#",
                "#....##.............#",
                "#.######.###.#.###..#",
                "#........#..........#",
                "#####################",
            ],
            True,
        ),
        (
            "One-step warehouse",
            [
                "#####",
                "#SG.#",
                "#####",
            ],
            True,
        ),
        (
            "Unreachable goal",
            [
                "#######",
                "#S....#",
                "###.###",
                "#...#G#",
                "#######",
            ],
            False,
        ),
    ]

    print("Warehouse Agent Test Suite")
    print("=" * 40)

    for title, grid, expected in test_cases:
        check_case(title, grid, expected)


if __name__ == "__main__":
    main()

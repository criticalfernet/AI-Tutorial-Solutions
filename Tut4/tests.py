from planner import (
    plan_with_bfs,
    warehouse_actions,
    simulate,
)


def run_case(title, initial, goal, actions, should_succeed):
    solution = plan_with_bfs(initial, actions, goal)

    exists = solution is not None
    passed = exists == should_succeed

    if passed and exists:
        state_sequence = simulate(initial, solution)
        passed = (
            state_sequence is not None
            and goal.issubset(state_sequence[-1])
        )

    print(f"{title}: {'PASS' if passed else 'FAIL'}")

    if solution is not None:
        print(
            "  Plan:",
            [action.label for action in solution]
        )


def main():
    initial_state = {
        "At(Robot,A)",
        "At(Package,A)"
    }

    goal_state = {
        "At(Package,C)"
    }

    run_case(
        "Test A - solvable warehouse",
        initial_state,
        goal_state,
        warehouse_actions(),
        True
    )

    run_case(
        "Test B - pickup unavailable",
        initial_state,
        goal_state,
        warehouse_actions(allow_pickup_at_a=False),
        False
    )

    run_case(
        "Test C - irrelevant action",
        initial_state,
        goal_state,
        warehouse_actions(add_wait_action=True),
        True
    )


if __name__ == "__main__":
    main()

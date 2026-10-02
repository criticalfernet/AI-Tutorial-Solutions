from collections import deque


class Action:
    def __init__(
        self,
        label,
        requires=None,
        forbids=None,
        adds=None,
        removes=None
    ):
        self.label = label
        self.requires = set(requires or ())
        self.forbids = set(forbids or ())
        self.adds = set(adds or ())
        self.removes = set(removes or ())

    def applicable(self, state):
        required_present = self.requires.issubset(state)
        forbidden_absent = self.forbids.isdisjoint(state)

        return required_present and forbidden_absent

    def execute(self, state):
        result = set(state)

        result.difference_update(self.removes)
        result.update(self.adds)

        return frozenset(result)


def plan_with_bfs(start_state, action_list, target):
    start_state = frozenset(start_state)
    target = set(target)

    if target.issubset(start_state):
        return []

    frontier = deque()
    frontier.append((start_state, []))

    explored = {start_state}

    while frontier:
        state, history = frontier.popleft()

        for action in action_list:
            if not action.applicable(state):
                continue

            successor = action.execute(state)

            if successor in explored:
                continue

            updated_history = history + [action]

            if target.issubset(successor):
                return updated_history

            explored.add(successor)
            frontier.append((successor, updated_history))

    return None


def warehouse_actions(
    allow_pickup_at_a=True,
    add_wait_action=False
):
    movement_actions = [
        Action(
            "Move(A, B)",
            requires={"At(Robot,A)"},
            adds={"At(Robot,B)"},
            removes={"At(Robot,A)"}
        ),
        Action(
            "Move(B, A)",
            requires={"At(Robot,B)"},
            adds={"At(Robot,A)"},
            removes={"At(Robot,B)"}
        ),
        Action(
            "Move(B, C)",
            requires={"At(Robot,B)"},
            adds={"At(Robot,C)"},
            removes={"At(Robot,B)"}
        ),
        Action(
            "Move(C, B)",
            requires={"At(Robot,C)"},
            adds={"At(Robot,B)"},
            removes={"At(Robot,C)"}
        ),
    ]

    pickup_actions = []

    if allow_pickup_at_a:
        pickup_actions.append(
            Action(
                "PickUp(Package, A)",
                requires={
                    "At(Robot,A)",
                    "At(Package,A)"
                },
                adds={"Holding(Package)"},
                removes={"At(Package,A)"}
            )
        )

    pickup_actions.extend([
        Action(
            "PickUp(Package, B)",
            requires={
                "At(Robot,B)",
                "At(Package,B)"
            },
            adds={"Holding(Package)"},
            removes={"At(Package,B)"}
        ),
        Action(
            "PickUp(Package, C)",
            requires={
                "At(Robot,C)",
                "At(Package,C)"
            },
            adds={"Holding(Package)"},
            removes={"At(Package,C)"}
        )
    ])

    drop_actions = [
        Action(
            "Drop(Package, A)",
            requires={
                "At(Robot,A)",
                "Holding(Package)"
            },
            adds={"At(Package,A)"},
            removes={"Holding(Package)"}
        ),
        Action(
            "Drop(Package, B)",
            requires={
                "At(Robot,B)",
                "Holding(Package)"
            },
            adds={"At(Package,B)"},
            removes={"Holding(Package)"}
        ),
        Action(
            "Drop(Package, C)",
            requires={
                "At(Robot,C)",
                "Holding(Package)"
            },
            adds={"At(Package,C)"},
            removes={"Holding(Package)"}
        )
    ]

    actions = movement_actions + pickup_actions + drop_actions

    if add_wait_action:
        actions.append(
            Action(
                "Wait(A)",
                requires={"At(Robot,A)"},
                adds={"At(Robot,A)"}
            )
        )

    return actions


def simulate(start, plan):
    current = frozenset(start)
    history = [current]

    for action in plan:
        if not action.applicable(current):
            return None

        current = action.execute(current)
        history.append(current)

    return history


def display_solution(initial, plan):
    if plan is None:
        print("No plan found.")
        return

    state_history = simulate(initial, plan)

    print("\nPlan:")
    for number, action in enumerate(plan, 1):
        print(f"{number}. {action.label}")

    print("\nState sequence:")

    for index, state in enumerate(state_history):
        print(f"S{index}: {sorted(state)}")

    goal_reached = "At(Package,C)" in state_history[-1]

    print("\nGoal achieved:", goal_reached)


def main():
    starting_state = {
        "At(Robot,A)",
        "At(Package,A)"
    }

    target_state = {
        "At(Package,C)"
    }

    available_actions = warehouse_actions()

    print("Logical Planning Agent")
    print("=" * 50)

    solution = plan_with_bfs(
        starting_state,
        available_actions,
        target_state
    )

    display_solution(starting_state, solution)


if __name__ == "__main__":
    main()

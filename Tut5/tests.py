from first_order import CORPUS, tokenise_corpus, estimate_transitions
from second_order import add_boundaries, train_second_order


TOLERANCE = 1e-9


def distributions_are_valid(model):
    for distribution in model.values():
        if abs(sum(distribution.values()) - 1.0) > TOLERANCE:
            return False

    return True


def test_first_order():
    sequences = tokenise_corpus(CORPUS)
    _, model = estimate_transitions(sequences)

    return distributions_are_valid(model)


def test_second_order():
    sequences = add_boundaries(CORPUS)
    _, model = train_second_order(sequences)

    return distributions_are_valid(model)


def report(name, passed):
    status = "PASS" if passed else "FAIL"
    print(f"{name}: {status}")


if __name__ == "__main__":
    report("First-order probability check", test_first_order())
    report("Second-order probability check", test_second_order())

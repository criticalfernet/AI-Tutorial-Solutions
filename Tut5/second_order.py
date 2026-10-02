from collections import Counter, defaultdict
import random


SAMPLES = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


def add_boundaries(sentences):
    sequences = []

    for text in sentences:
        tokens = text.lower().split()
        sequences.append(["<START>", "<START>", *tokens, "<END>"])

    return sequences


def train_second_order(sequences):
    counts = defaultdict(Counter)

    for tokens in sequences:
        for position in range(2, len(tokens)):
            history = (tokens[position - 2], tokens[position - 1])
            target = tokens[position]
            counts[history][target] += 1

    model = {}

    for history, next_tokens in counts.items():
        total = sum(next_tokens.values())

        model[history] = {
            token: frequency / total
            for token, frequency in next_tokens.items()
        }

    return counts, model


def choose_greedy(model, history):
    distribution = model.get(history)

    if not distribution:
        return None

    return max(distribution, key=distribution.get)


def choose_sample(model, history):
    distribution = model.get(history)

    if not distribution:
        return None

    candidates = list(distribution.keys())
    probabilities = list(distribution.values())

    return random.choices(
        candidates,
        weights=probabilities,
        k=1
    )[0]


def generate(model, deterministic=False, maximum=20):
    history = ("<START>", "<START>")
    generated = []

    for _ in range(maximum):
        if deterministic:
            token = choose_greedy(model, history)
        else:
            token = choose_sample(model, history)

        if token is None or token == "<END>":
            break

        generated.append(token)
        history = (history[1], token)

    return " ".join(generated)


def show_distribution(model, history):
    print(f"\nP(next | {history})")

    distribution = model.get(history, {})

    for token, probability in sorted(distribution.items()):
        print(f"  {token:8s}: {probability:.3f}")


def main():
    random.seed(11)

    sequences = add_boundaries(SAMPLES)
    counts, model = train_second_order(sequences)

    print("Second-order autoregressive model")
    print("=" * 50)

    examples = [
        ("the", "cat"),
        ("the", "dog"),
        ("cat", "ran"),
        ("dog", "sat"),
        ("sat", "on"),
    ]

    for history in examples:
        show_distribution(model, history)

    print("\nConditional probability checks")

    for history, distribution in model.items():
        total = sum(distribution.values())
        print(f"{history}: {total:.3f}")

    print("\nSampled sentences")

    for _ in range(10):
        print(generate(model))


if __name__ == "__main__":
    main()

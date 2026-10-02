from collections import Counter, defaultdict
import random


CORPUS = [
    "the cat sat on the mat",
    "the cat sat on the rug",
    "the dog sat on the mat",
    "the dog ran to the park",
    "the cat ran to the park",
    "the dog sat on the rug",
]


def tokenise_corpus(lines):
    result = []

    for line in lines:
        tokens = line.lower().split()
        result.append(["<START>", *tokens, "<END>"])

    return result


def estimate_transitions(tokenised_sentences):
    counts = defaultdict(Counter)

    for sequence in tokenised_sentences:
        for previous, following in zip(sequence[:-1], sequence[1:]):
            counts[previous][following] += 1

    distributions = {}

    for previous, next_counts in counts.items():
        total = sum(next_counts.values())

        distributions[previous] = {
            token: frequency / total
            for token, frequency in next_counts.items()
        }

    return counts, distributions


def greedy_choice(distributions, context):
    options = distributions.get(context)

    if not options:
        return None

    return max(options, key=options.get)


def random_choice(distributions, context):
    options = distributions.get(context)

    if not options:
        return None

    tokens = tuple(options.keys())
    probabilities = tuple(options.values())

    return random.choices(
        population=tokens,
        weights=probabilities,
        k=1
    )[0]


def generate_text(distributions, deterministic=False, limit=20):
    context = "<START>"
    output = []

    for _ in range(limit):
        if deterministic:
            token = greedy_choice(distributions, context)
        else:
            token = random_choice(distributions, context)

        if token is None or token == "<END>":
            break

        output.append(token)
        context = token

    return " ".join(output)


def display_distributions(distributions, contexts):
    for context in contexts:
        print(f"\nP(next | {context})")

        if context not in distributions:
            print("  no recorded transitions")
            continue

        entries = sorted(distributions[context].items())

        for token, probability in entries:
            print(f"  {token:8s}: {probability:.3f}")


def main():
    random.seed(7)

    dataset = tokenise_corpus(CORPUS)
    counts, probabilities = estimate_transitions(dataset)

    print("First-order autoregressive model")
    print("=" * 50)

    display_distributions(
        probabilities,
        ["the", "cat", "dog", "sat", "ran"]
    )

    print("\nConditional probability checks")
    for context, distribution in probabilities.items():
        total = sum(distribution.values())
        print(f"{context:8s}: {total:.3f}")

    print("\nGreedy next-token predictions")
    for context in ["the", "cat", "dog", "sat", "ran"]:
        print(f"{context:8s} -> {greedy_choice(probabilities, context)}")

    print("\nGreedy generation")
    for _ in range(5):
        print(generate_text(probabilities, deterministic=True))

    print("\nSampling generation")
    for _ in range(20):
        print(generate_text(probabilities))


if __name__ == "__main__":
    main()

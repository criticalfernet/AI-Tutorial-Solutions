# Bayesian Networks and Autoregressive Language Models

This project contains the laboratory implementation of Bayesian-network-style probability tables and autoregressive language models.

The experiments begin with a first-order model based on the previous token and then extend it to a second-order model using two-token contexts. The repository also compares greedy generation with random sampling and verifies that the learned conditional distributions are properly normalized.

## Dataset

The experiments use the six sentences provided in the laboratory:

```text
the cat sat on the mat
the cat sat on the rug
the dog sat on the mat
the dog ran to the park
the cat ran to the park
the dog sat on the rug
```

Before training, each sentence is converted to lowercase and wrapped with `<START>` and `<END>` markers.

These boundary tokens allow the models to represent both the beginning and termination of a sentence.

---

## First-Order Model

The first implementation considers only the immediately preceding token when predicting the next one:

```text
P(Xt | Xt-1)
```

For every pair of consecutive tokens, the program records its frequency:

```text
C(previous, next)
```

The transition probabilities are then obtained by normalizing the counts associated with each previous token:

```text
P(next | previous)
    = C(previous, next)
      -------------------
      Σk C(previous, k)
```

Thus, each previous token defines a conditional probability distribution over possible next tokens.

Run the implementation with:

```bash
python first_order.py
```

The program reports selected transition probabilities, verifies their normalization, performs deterministic generation, and produces randomly sampled sentences.

---

## Second-Order Model

The second implementation retains two previous tokens as the context:

```text
P(Xt | Xt-2, Xt-1)
```

Instead of a single previous word, the context is therefore represented as an ordered pair:

```text
(previous_previous, previous)
```

Transition counts are collected separately for each such pair and normalized to form the corresponding conditional distributions.

Run it using:

```bash
python second_order.py
```

The resulting dependency structure can be viewed as two previous variables providing information about the current variable.

---

## Sentence Generation

Two generation strategies are implemented.

### Greedy generation

At every step, the token with the highest conditional probability is selected:

```text
next = argmax P(next | context)
```

Since the same highest-probability choice is made whenever the same context occurs, greedy generation is deterministic.

### Probabilistic generation

Instead of selecting only the most likely token, sampling draws the next token according to the complete conditional distribution.

For example, a distribution such as:

```text
cat   → 0.6
dog   → 0.3
bird  → 0.1
```

allows all three tokens to be selected, although `cat` occurs most frequently.

This makes sampled sentences less predictable and provides greater variation across multiple generations.

---

## Probability Validation

Every conditional probability table must satisfy:

```text
Σv P(v | context) = 1
```

The repository includes a test program that checks this property for both models.

Run:

```bash
python tests.py
```

A context whose probabilities do not sum to approximately one indicates an error in the construction or normalization of its conditional distribution.

The test therefore acts as a basic consistency check on the learned probability tables.

---

## Comparing the Two Models

| Property                  | First-order          | Second-order            |
| ------------------------- | -------------------- | ----------------------- |
| Context size              | 1 token              | 2 tokens                |
| Conditional probability   | `P(next \| current)` | `P(next \| previous 2)` |
| Available context         | Smaller              | Larger                  |
| Number of contexts        | Lower                | Higher                  |
| Training-data requirement | Lower                | Higher                  |
| Sparse contexts           | Less common          | More common             |

The second-order model can distinguish contexts that look identical when only the most recent token is considered.

However, increasing the context size also increases the number of possible context combinations. With a small dataset, many of these combinations may occur rarely or not at all.

This illustrates the basic trade-off between **more contextual information** and **data sparsity**.

---

## Relation to Autoregressive Language Modeling

Both models follow the same general autoregressive idea:

```text
predict the next token using previously observed tokens
```

The difference is how much history is retained.

The first-order model uses:

```text
one previous token
```

while the second-order model uses:

```text
two previous tokens
```

This makes the laboratory a simple demonstration of how increasing the available history changes a probabilistic sequence model.

---

## Repository Contents

```text
first_order.py
second_order.py
tests.py
lab_answers.md
README.md
.gitignore
```

The Python files contain the model implementations and validation experiments, while `lab_answers.md` contains the written responses and observations required by the laboratory.

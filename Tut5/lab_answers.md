# Lab Answers

## 1. Why use the chain rule?

The chain rule expresses the probability of an entire sequence as a product of conditional probabilities. For a sentence, this means the model can determine the probability of the sequence by predicting one token at a time from the tokens that came before it.

This same formulation also provides a natural way to generate text sequentially.

---

## 2. First-order assumption

A first-order model makes a Markov-style assumption that only the most recent token matters when predicting the next one:

```text
P(Xt | X1, X2, ..., Xt-1) = P(Xt | Xt-1)
```

Therefore, all earlier tokens are ignored once `Xt-1` is known.

---

## 3. Selected conditional probabilities

Using the supplied training corpus, some of the resulting transition distributions are:

```text
Given "the":

cat   = 0.25
dog   = 0.25
mat   = 0.1667
rug   = 0.1667
park  = 0.1667
```

For the contexts `cat` and `dog`:

```text
P(next | cat):
sat = 0.6667
ran = 0.3333

P(next | dog):
sat = 0.6667
ran = 0.3333
```

The remaining examples are:

```text
P(next | sat):
on = 1.0

P(next | ran):
to = 1.0
```

Any transition that never occurs in the corpus receives probability zero.

---

## 4. Where are the transition counts stored?

The transition frequencies are maintained in `first_order.py` using a nested counting structure:

```text
defaultdict(Counter)
```

The outer key represents the current context token, while the associated `Counter` records how frequently each possible next token follows it.

---

## 5. Constructing the CPT

For a particular context, the program first obtains the counts of all observed next tokens.

The probability of each possible successor is then calculated by dividing its count by the total number of transitions leaving that context:

```text
P(next | context)
    = count(context, next)
      ----------------------
      total transitions
```

The resulting values form the conditional probability table.

---

## 6. Generation methods

The implementation provides two ways of generating a sequence.

**Greedy generation**

The token with the largest conditional probability is selected at every step.

```text
next = argmax P(next | context)
```

For a fixed model and starting condition, this produces the same sequence.

**Sampling**

Instead of always taking the largest probability, the next token is randomly drawn according to the learned distribution.

Consequently, repeated runs can generate different sentences.

---

## 7. What happens when generation reaches an unknown context?

If the current token does not have any recorded outgoing transition, there is no probability distribution from which the next token can be selected.

The implementation therefore returns `None` and terminates generation.

---

## 8. Interpreting an invalid probability sum

For any fixed context, the probabilities over all possible next tokens should satisfy:

```text
Σ P(next | context) ≈ 1
```

Therefore, obtaining a value such as `0.87` indicates that the corresponding conditional distribution was constructed or normalized incorrectly.

---

## 9. Can the model predict what a human would naturally expect?

Not necessarily.

The model has access only to the statistical patterns contained in its training corpus. A human can use additional grammatical, semantic, and world knowledge that is absent from this small dataset.

Consequently, a human's expected continuation may have little or no probability under the learned model.

---

## 10. Why does sampling generate more varied text?

Greedy generation always selects the locally highest-probability continuation. If the same context occurs again, the same decision is made again.

Sampling considers the entire probability distribution instead. Lower-probability alternatives therefore have a chance of being selected, producing different sequences across runs.

With a small model, greedy selection can also repeatedly follow the same high-probability transitions and produce repetitive output.

---

## 11. Characteristics of a second-order model

A second-order model changes the dependency structure so that the next token depends on the previous two tokens:

```text
P(Xt | Xt-2, Xt-1)
```

Compared with the first-order model, it therefore:

1. uses two preceding tokens as context;
2. records transition counts for token pairs;
3. has more information available when predicting the next token;
4. has more possible contexts to estimate.

The final point means that a larger training corpus is generally needed to obtain reliable estimates.

---

## 12. Effect of increasing the context size

Using additional history can improve predictions because two occurrences of the same final token may require different predictions depending on what appeared immediately before it.

For example, a first-order model treats both situations with the same most recent token as identical. A second-order model can separate them.

The drawback is data sparsity: increasing the context length creates more possible conditional contexts, many of which may have few or zero observations.

---

## 13. Why specify the probability model precisely?

A precise mathematical specification removes ambiguity about what the implementation is supposed to represent.

It also makes the resulting program easier to inspect and test. For example, the transition-count representation, normalization rule, and independence assumptions can each be checked against the specification.

This helps distinguish an implementation of the intended probabilistic model from one that merely produces plausible-looking text.

---

## 14. Bayesian-network interpretation

Viewing the autoregressive model as a Bayesian network makes several properties explicit:

* the dependencies between variables are clearly represented;
* the joint probability can be factorized into conditional terms;
* each CPT has a direct probabilistic interpretation;
* generation follows the dependency structure of the network;
* the conditional-independence assumptions become easier to identify.

Thus, the Bayesian-network perspective provides a structured way to understand both the probability calculations and the assumptions behind the model.

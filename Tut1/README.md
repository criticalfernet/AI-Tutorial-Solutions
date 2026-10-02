# Neural Models Lab

This repository contains the implementation for the Neural Models laboratory conducted on **August 7, 2026**.

The lab uses a very small XOR problem to study why a nonlinear hidden layer is needed, how the output layer and loss are chosen, how backpropagation appears in PyTorch, and how different initialization and activation choices affect learning. The later part extends the same input to a three-class problem.

## Setup

The experiments were written in Python and use:

* Python 3
* PyTorch
* NumPy


## Repository Contents

```text
Tut1/
├── xor_experiment.py
├── activation_experiment.py
├── symmetry_experiment.py
├── three_class.py
├── results.txt
├── README.md
└── .gitignore
```

---

## XOR Classification

The first experiment uses the standard XOR truth table:

| Input 1 | Input 2 | Output |
| ------: | ------: | -----: |
|       0 |       0 |      0 |
|       0 |       1 |      1 |
|       1 |       0 |      1 |
|       1 |       1 |      0 |

The network consists of two input values, a hidden layer containing two neurons, and a single output neuron:

```text
Input (2) → Hidden Layer (2) → Output (1)
```

`tanh` is used in the hidden layer. The output layer produces a logit, and `BCEWithLogitsLoss` is used for training. This combines the sigmoid operation and binary cross-entropy loss in a numerically stable form.

Execute the experiment using:

```bash
python xor_experiment.py
```

The script displays the loss before and after training, predicted probabilities, predicted classes, classification accuracy, and the gradients of the first layer.

---

## Symmetry

The second experiment investigates what happens when every network weight is initialized to zero.

```bash
python symmetry_experiment.py
```

The two hidden neurons begin with exactly the same parameters. Since they also receive the same inputs, their gradients remain identical during training. As a result, the neurons continue to behave identically instead of learning separate representations.

This demonstrates why breaking symmetry through initialization is important when training neural networks. The zero-initialization experiment is specifically required by the laboratory instructions.

---

## Comparing Activation Functions

The next experiment repeats the XOR task with three different hidden-layer activations:

1. Sigmoid
2. `tanh`
3. ReLU

Run it with:

```bash
python activation_experiment.py
```

For every activation function, the program records quantities such as:

* Final training loss
* Number of correctly classified samples
* Gradient magnitude during the early stages of training

The experiment illustrates how the derivative of an activation function affects the gradients propagated through the network. However, the results are specific to this small XOR setup and should not be interpreted as proof that one activation function is always superior to the others.

---

## Extending XOR to Three Classes

The final classification experiment changes the original binary problem into a three-class problem.

The labels are assigned as follows:

```text
(0,0) → Class 0
(0,1) → Class 1
(1,0) → Class 1
(1,1) → Class 2
```

Because there are now three possible classes, the network produces three output logits:

```text
Input → Hidden Layer → [logit₀, logit₁, logit₂]
```

Multiclass cross-entropy is used as the training objective. During evaluation, the logits are converted into probabilities using softmax.

Run:

```bash
python three_class.py
```

The script prints the probability distribution predicted for each input and also verifies that the probabilities for an example input add up to approximately one.

---

## Backpropagation in PyTorch

Training follows the usual neural-network workflow:

```text
Input
  ↓
Forward pass
  ↓
Compute loss
  ↓
Clear old gradients
  ↓
Backpropagation
  ↓
Update parameters
```

In PyTorch, the important operation is:

```python
loss.backward()
```

This calculates the derivatives of the loss with respect to the parameters involved in the computation.

For example:

```python
model.hidden.weight.grad
```

gives the gradient of the loss with respect to the weights connecting the input layer to the hidden layer.

The experiment therefore provides a direct way of observing the chain rule and backpropagation rather than treating them as purely mathematical concepts.

---

## Why the Hidden Layer Needs an Activation

XOR cannot be represented by a single linear decision boundary.

Adding multiple layers does not solve this if every layer is only an affine transformation. Multiple affine transformations can be combined into one equivalent affine transformation.

The nonlinear activation in the hidden layer changes this. It allows the network to transform the original input into a representation from which the XOR relationship can be separated.

This is the main idea demonstrated by the first experiment.

---

## Key Takeaways

The experiments demonstrate several important neural-network concepts:

* XOR requires a nonlinear transformation to be represented by this network.
* Loss and prediction accuracy provide useful evidence about whether training is actually working.
* Initializing identical hidden neurons identically can cause them to remain symmetric.
* Activation functions influence the gradients flowing through the network.
* The number and type of output units depend on the classification problem.
* Binary classification and multiclass classification use different output/loss configurations.
* Backpropagation in PyTorch can be inspected directly through parameter gradients.

## Running the Experiments

All four experiments can be run individually:

```bash
python xor_experiment.py
python symmetry_experiment.py
python activation_experiment.py
python three_class.py
```

The outputs from the completed runs are stored in:

```text
results.txt
```

The implementation is deliberately small so that the individual steps of forward propagation, loss calculation, gradient computation, and parameter updates can be examined without the distraction of a larger neural-network framework.

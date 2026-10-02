import torch
import torch.nn as nn

torch.set_num_threads(1)


inputs = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
])

targets = torch.tensor([
    [0.0],
    [1.0],
    [1.0],
    [0.0]
])


class XORClassifier(nn.Module):
    def __init__(self, activation_name="tanh"):
        super().__init__()

        self.layer1 = nn.Linear(2, 2)
        self.layer2 = nn.Linear(2, 1)

        activations = {
            "sigmoid": nn.Sigmoid(),
            "tanh": nn.Tanh(),
            "relu": nn.ReLU()
        }

        if activation_name not in activations:
            raise ValueError(f"Unsupported activation: {activation_name}")

        self.activation = activations[activation_name]

    def forward(self, inputs):
        hidden_output = self.layer1(inputs)
        hidden_output = self.activation(hidden_output)

        return self.layer2(hidden_output)


def run_training(
    seed=0,
    activation="tanh",
    iterations=5000,
    learning_rate=0.1
):
    torch.manual_seed(seed)

    network = XORClassifier(activation)
    criterion = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(
        network.parameters(),
        lr=learning_rate
    )

    first_loss = None
    first_layer_gradient = None

    for iteration in range(iterations):
        outputs = network(inputs)
        current_loss = criterion(outputs, targets)

        if iteration == 0:
            first_loss = current_loss.item()

        optimizer.zero_grad()
        current_loss.backward()

        if iteration == 0:
            first_layer_gradient = (
                network.layer1.weight.grad.detach().clone()
            )

        optimizer.step()

    with torch.no_grad():
        probabilities = torch.sigmoid(network(inputs)).flatten()
        predictions = (probabilities >= 0.5).to(torch.int32)

    return (
        network,
        first_loss,
        current_loss.item(),
        probabilities,
        predictions,
        first_layer_gradient
    )


if __name__ == "__main__":
    (
        network,
        initial_loss,
        final_loss,
        probabilities,
        predictions,
        gradient
    ) = run_training()

    print("XOR Neural Network")
    print("=" * 45)

    print("Architecture: 2 -> 2 -> 1")
    print("Hidden activation: tanh")
    print("Training loss: BCEWithLogitsLoss")
    print()

    print(f"Initial loss: {initial_loss:.6f}")
    print(f"Final loss:   {final_loss:.6f}")
    print(
        f"Early ||gradient W1||: "
        f"{gradient.norm().item():.6f}"
    )

    print()
    print("Input       Probability    Prediction")

    for sample, probability, prediction in zip(
        inputs,
        probabilities,
        predictions
    ):
        print(
            f"{sample.tolist()}     "
            f"{probability.item():.6f}       "
            f"{prediction.item()}"
        )

    correct = (
        predictions == targets.flatten().to(torch.int32)
    ).sum().item()

    print(f"\nCorrect predictions: {correct}/4")

    print("\nFirst-layer gradient tensor from the first backward pass:")
    print(gradient)

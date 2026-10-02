import torch
import torch.nn as nn

torch.set_num_threads(1)


samples = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
])

targets = torch.tensor([0, 1, 1, 0])


class XORModel(nn.Module):
    def __init__(self, activation_fn):
        super().__init__()

        self.hidden_layer = nn.Linear(2, 2)
        self.output_layer = nn.Linear(2, 1)
        self.activation_fn = activation_fn

    def forward(self, x):
        x = self.hidden_layer(x)
        x = self.activation_fn(x)
        return self.output_layer(x)


activation_functions = {
    "sigmoid": nn.Sigmoid(),
    "tanh": nn.Tanh(),
    "relu": nn.ReLU()
}

seeds = {
    "sigmoid": 1,
    "tanh": 0,
    "relu": 2
}

print("Activation Experiment")
print("=" * 45)


for name, seed in seeds.items():

    torch.manual_seed(seed)

    network = XORModel(activation_functions[name])
    criterion = nn.BCEWithLogitsLoss()

    optimizer = torch.optim.Adam(
        network.parameters(),
        lr=0.1
    )

    first_gradient_size = None

    for iteration in range(5000):

        output = network(samples)
        loss = criterion(
            output,
            targets.float().reshape(-1, 1)
        )

        optimizer.zero_grad()
        loss.backward()

        if iteration == 0:
            first_gradient_size = (
                network.hidden_layer.weight.grad.norm().item()
            )

        optimizer.step()

    with torch.no_grad():
        probability = torch.sigmoid(network(samples)).flatten()
        predicted_class = (probability >= 0.5).to(torch.int32)

    number_correct = (
        predicted_class == targets
    ).sum().item()

    print(
        f"{name:8s} "
        f"loss={loss.item():.6f} "
        f"correct={number_correct}/4 "
        f"early_grad={first_gradient_size:.6f}"
    )

    print(
        "  probabilities:",
        [round(value.item(), 4) for value in probability]
    )

import torch
import torch.nn as nn

torch.set_num_threads(1)


# XOR samples
data = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
])

labels = torch.tensor([
    [0.0],
    [1.0],
    [1.0],
    [0.0]
])


class SymmetryNet(nn.Module):
    def __init__(self):
        super().__init__()

        self.first_layer = nn.Linear(2, 2)
        self.final_layer = nn.Linear(2, 1)

    def forward(self, data):
        hidden = torch.sigmoid(self.first_layer(data))
        return self.final_layer(hidden)


network = SymmetryNet()

# Start every trainable parameter from exactly zero.
with torch.no_grad():
    for weight in network.parameters():
        weight.fill_(0.0)


criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.SGD(
    network.parameters(),
    lr=0.5
)


def show_hidden_weights(title):
    print(title)
    print(network.first_layer.weight)

print("Symmetry Experiment")
print("=" * 45)

show_hidden_weights("Hidden weights at initialization:")

for iteration in range(5):
    predictions = network(data)
    error = criterion(predictions, labels)

    optimizer.zero_grad()
    error.backward()
    optimizer.step()

    print(f"\nAfter update {iteration + 1}:")
    print(network.first_layer.weight)


print("\nObservation:")
print("Both hidden neurons continue to have identical weights.")
print(
    "Since they start with the same parameters and receive the same "
    "gradients, training does not break the symmetry between them."
)
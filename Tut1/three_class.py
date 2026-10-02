import torch
import torch.nn as nn

torch.set_num_threads(1)


inputs = torch.tensor([
    [0.0, 0.0],
    [0.0, 1.0],
    [1.0, 0.0],
    [1.0, 1.0]
])

classes = torch.tensor([0, 1, 1, 2])


class MultiClassXOR(nn.Module):
    def __init__(self):
        super().__init__()

        self.feature_layer = nn.Linear(2, 2)
        self.classifier = nn.Linear(2, 3)

    def forward(self, inputs):
        features = torch.tanh(self.feature_layer(inputs))
        return self.classifier(features)


torch.manual_seed(42)

network = MultiClassXOR()

criterion = nn.CrossEntropyLoss()

optimizer = torch.optim.Adam(
    network.parameters(),
    lr=0.1
)


num_epochs = 3000

for epoch in range(num_epochs):
    scores = network(inputs)
    error = criterion(scores, classes)

    optimizer.zero_grad()
    error.backward()
    optimizer.step()


with torch.no_grad():
    scores = network(inputs)
    class_probabilities = torch.softmax(scores, dim=1)
    predicted_classes = torch.argmax(class_probabilities, dim=1)


print("Three-Class XOR Experiment")
print("=" * 45)
print(f"Final training loss: {error.item():.6f}")
print()

for sample, probs, predicted in zip(
    inputs,
    class_probabilities,
    predicted_classes
):
    formatted_probs = [
        round(prob.item(), 4)
        for prob in probs
    ]

    print(
        f"{sample.tolist()} -> "
        f"{formatted_probs}, "
        f"predicted class = {predicted.item()}"
    )


probability_total = class_probabilities[0].sum().item()

print(
    "\nProbability sum for first example:",
    round(probability_total, 6)
)

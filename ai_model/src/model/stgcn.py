import torch
import torch.nn as nn


class SimpleSTGCN(nn.Module):
    def __init__(self, num_joints: int, num_classes: int):
        super(SimpleSTGCN, self).__init__()

        # Temporal Conv (على الزمن)
        self.temporal_conv1 = nn.Conv2d(
            in_channels=3,
            out_channels=64,
            kernel_size=(3, 1),
            padding=(1, 0),
        )

        self.temporal_conv2 = nn.Conv2d(
            in_channels=64,
            out_channels=128,
            kernel_size=(3, 1),
            padding=(1, 0),
        )

        # Fully Connected
        self.fc = nn.Linear(128 * num_joints, num_classes)

        self.relu = nn.ReLU()

    def forward(self, x):
        """
        x shape:
        (batch, channels, time, joints)

        channels = 3 (x, y, z)
        """

        # Conv layers
        x = self.relu(self.temporal_conv1(x))
        x = self.relu(self.temporal_conv2(x))

        # flatten
        x = x.mean(dim=2)  # average over time
        x = x.view(x.size(0), -1)

        # classification
        x = self.fc(x)

        return x
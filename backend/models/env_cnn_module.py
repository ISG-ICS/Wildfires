from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import torch.nn as nn
import torch.nn.functional as F


class CNN(nn.Module):

    def __init__(self, n_channels=8):
        """
        Initializes CNN object.

        Args:
          n_channels: number of input channels
          n_classes: number of classes of the classification problem
        """
        super(CNN, self).__init__()
        self.conv1 = nn.Conv2d(n_channels, 100, (1,1))

#         self.conv2 = nn.Conv2d(100, 1, (1,1))
        self.conv2 = nn.Conv2d(100, 2, (1,1))


    def forward(self, x):
        """
        Performs forward pass of the input.

        Args:
          x: input to the network
        Returns:
          out: outputs of the network
        """
        x = F.relu(self.conv1(x))

        out = F.relu(self.conv2(x))

        # x = x.view(-1, 512)
        #     print(x.shape)

        return out

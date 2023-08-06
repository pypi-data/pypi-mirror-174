#!/usr/bin/env python3

"""References:

- https://github.com/luuuyi/CBAM.PyTorch/blob/master/model/resnet_cbam.py
"""

import math

import torch
import torch.nn as nn
import torch.nn.functional as F


class BaseBletteAttentionModule(nn.Module):
    def __init__(self):
        super().__init__()

    def init_weights(self):
        for m in self.modules():
            if isinstance(m, nn.Conv2d):
                n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                m.weight.data.normal_(0, math.sqrt(2.0 / n))
            elif isinstance(m, nn.BatchNorm2d):
                m.weight.data.fill_(1)
                m.bias.data.zero_()

    def forward(self, x):
        raise NotImplementedError


class ChannelAttention(BaseBletteAttentionModule):
    def __init__(self, in_planes, ratio=16):
        super().__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)
        self.max_pool = nn.AdaptiveMaxPool2d(1)
        self.fc = nn.Sequential(
            nn.Conv2d(in_planes, in_planes // ratio, 1, bias=False),
            nn.ReLU(),
            nn.Conv2d(in_planes // ratio, in_planes, 1, bias=False),
        )

    def forward(self, x):
        avg_out = self.fc(self.avg_pool(x))
        max_out = self.fc(self.max_pool(x))
        out = avg_out + max_out
        return torch.sigmoid(out)


class SpatialAttention(BaseBletteAttentionModule):
    def __init__(self, kernel_size=7):
        super().__init__()
        self.conv1 = nn.Conv2d(2, 1, kernel_size, padding=kernel_size // 2, bias=False)

    def forward(self, x):
        avg_out = torch.mean(x, dim=1, keepdim=True)
        max_out, _ = torch.max(x, dim=1, keepdim=True)
        x = torch.cat([avg_out, max_out], dim=1)
        x = self.conv1(x)
        return torch.sigmoid(x)


class SASA_Layer(BaseBletteAttentionModule):
    def __init__(
        self, in_channels, kernel_size=7, num_heads=8, image_size=224, inference=False
    ):
        super().__init__()
        self.kernel_size = min(
            kernel_size, image_size
        )  # receptive field shouldn't be larger than input H/W
        self.num_heads = num_heads
        self.dk = self.dv = in_channels
        self.dkh = self.dk // self.num_heads
        self.dvh = self.dv // self.num_heads

        assert (
            self.dk % self.num_heads == 0
        ), "dk should be divided by num_heads. (example: dk: 32, num_heads: 8)"
        assert (
            self.dk % self.num_heads == 0
        ), "dv should be divided by num_heads. (example: dv: 32, num_heads: 8)"

        self.k_conv = nn.Conv2d(self.dk, self.dk, kernel_size=1)
        self.q_conv = nn.Conv2d(self.dk, self.dk, kernel_size=1)
        self.v_conv = nn.Conv2d(self.dv, self.dv, kernel_size=1)

        # Positional encodings
        self.rel_encoding_h = nn.Parameter(
            torch.randn(self.dk // 2, self.kernel_size, 1), requires_grad=True
        )
        self.rel_encoding_w = nn.Parameter(
            torch.randn(self.dk // 2, 1, self.kernel_size), requires_grad=True
        )

        # later access attention weights
        self.inference = inference
        if self.inference:
            self.register_parameter("weights", None)

    def forward(self, x):
        batch_size, _, height, width = x.size()

        # Compute k, q, v
        padded_x = F.pad(
            x,
            [
                (self.kernel_size - 1) // 2,
                (self.kernel_size - 1) - ((self.kernel_size - 1) // 2),
                (self.kernel_size - 1) // 2,
                (self.kernel_size - 1) - ((self.kernel_size - 1) // 2),
            ],
        )
        k = self.k_conv(padded_x)
        q = self.q_conv(x)
        v = self.v_conv(padded_x)

        # Unfold patches into [BS, num_heads*depth, horizontal_patches, vertical_patches, kernel_size, kernel_size]
        k = k.unfold(2, self.kernel_size, 1).unfold(3, self.kernel_size, 1)
        v = v.unfold(2, self.kernel_size, 1).unfold(3, self.kernel_size, 1)

        # Reshape into [BS, num_heads, horizontal_patches, vertical_patches, depth_per_head, kernel_size*kernel_size]
        k = k.reshape(batch_size, self.num_heads, height, width, self.dkh, -1)
        v = v.reshape(batch_size, self.num_heads, height, width, self.dvh, -1)

        # Reshape into [BS, num_heads, height, width, depth_per_head, 1]
        q = q.reshape(batch_size, self.num_heads, height, width, self.dkh, 1)

        qk = torch.matmul(q.transpose(4, 5), k)
        qk = qk.reshape(
            batch_size,
            self.num_heads,
            height,
            width,
            self.kernel_size,
            self.kernel_size,
        )

        # Add positional encoding
        qr_h = torch.einsum("bhxydz,cij->bhxyij", q, self.rel_encoding_h)
        qr_w = torch.einsum("bhxydz,cij->bhxyij", q, self.rel_encoding_w)
        qk += qr_h
        qk += qr_w

        qk = qk.reshape(
            batch_size,
            self.num_heads,
            height,
            width,
            1,
            self.kernel_size * self.kernel_size,
        )
        weights = torch.softmax(qk, dim=-1)

        if self.inference:
            self.weights = nn.Parameter(weights)

        attn_out = torch.matmul(weights, v.transpose(4, 5))
        attn_out = attn_out.reshape(batch_size, -1, height, width)
        return attn_out

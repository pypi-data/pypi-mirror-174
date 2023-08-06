#!/usr/bin/env python3

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule


class GroupedConvFuse(nn.Module):
    """Basic multi-layer side fusion used in CaseNet

    https://github.com/Lavender105/DFF/blob/master/exps/models/casenet.py

    Changes:
    - bias=False: no bias in the last layer
    - flexible: number of sides could channge (CASENet, DDS, etc...)
    """

    def __init__(
        self,
        num_classes,
        num_sides,
        conv_cfg=None,
        bias=True,
    ):
        super().__init__()

        self.num_sides = num_sides

        # fuse (grouped convolution)
        self.fuse = ConvModule(
            in_channels=num_classes * num_sides,
            out_channels=num_classes,
            kernel_size=1,
            groups=num_classes,
            conv_cfg=conv_cfg,
            norm_cfg=None,
            bias=bias,  # originally True
            act_cfg=None,
        )

    def forward(self, sides):
        assert isinstance(sides, list)
        assert len(sides) == self.num_sides, f"number of sides: {len(sides)}"

        side5 = sides.pop(-1)

        slice5 = side5[:, 0:1, :, :]
        fuse = torch.cat((slice5, *sides), 1)
        for i in range(side5.size(1) - 1):
            slice5 = side5[:, i + 1 : i + 2, :, :]
            fuse = torch.cat((fuse, slice5, *sides), 1)

        fuse = self.fuse(fuse)

        return fuse


class GroupedConvFuseSide4(GroupedConvFuse):
    def forward(self, sides):
        assert isinstance(sides, list)
        assert len(sides) == self.num_sides, f"number of sides: {len(sides)}"

        side5 = sides.pop(-1)
        side4 = sides.pop(-1)

        slice5 = side5[:, 0:1, :, :]
        slice4 = side4[:, 0:1, :, :]
        fuse = torch.cat((slice5, slice4, *sides), 1)
        for i in range(side5.size(1) - 1):
            slice5 = side5[:, i + 1 : i + 2, :, :]
            slice4 = side4[:, i + 1 : i + 2, :, :]
            fuse = torch.cat((fuse, slice5, slice4, *sides), 1)

        fuse = self.fuse(fuse)

        return fuse


class LocationAdaptiveLearner(nn.Module):
    """LocationAdaptiveLearner

    https://github.com/Lavender105/DFF/blob/master/exps/models/dff.py
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        conv_cfg,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
    ):
        super().__init__()

        self.conv_layers = nn.Sequential(
            nn.ReLU(),  # NOTE: added activation
            ConvModule(
                in_channels,
                out_channels,
                1,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=act_cfg,
            ),
            ConvModule(
                out_channels,
                out_channels,
                1,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=act_cfg,
            ),
            ConvModule(
                out_channels,
                out_channels,
                1,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=None,
            ),
            nn.Sigmoid(),
        )

    def forward(self, inputs):
        assert isinstance(inputs, (list, tuple))
        assert len(inputs) == 5

        side1, side2, side3, side5, side5_w = inputs
        num_backbone = 4
        num_classes = side5.size(1)

        slice5 = side5[:, 0:1, :, :]
        fuse = torch.cat((slice5, side1, side2, side3), 1)
        for i in range(side5.size(1) - 1):
            slice5 = side5[:, i + 1 : i + 2, :, :]
            fuse = torch.cat((fuse, slice5, side1, side2, side3), 1)

        # (N, 19*4, H, W)
        w = self.conv_layers(side5_w)
        # Reshape to (N, 19, 4, H, W)
        w = w.view(w.size(0), num_classes, num_backbone, w.size(2), w.size(3))
        fuse = fuse.view(fuse.size(0), num_classes, -1, fuse.size(2), fuse.size(3))

        # fuse = torch.mul(fuse, w)
        # fuse = torch.sum(fuse, 2)
        # fuse = fuse * torch.sigmoid(w)
        fuse = fuse * w
        fuse = torch.sum(fuse, 2)

        return fuse

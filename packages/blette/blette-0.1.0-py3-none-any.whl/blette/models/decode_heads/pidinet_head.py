#!/usr/bin/env python3

"""PiDiNet Head

https://github.com/zhuoinoulu/pidinet
"""

import torch
import torch.nn as nn

from mmseg.ops import resize

from .multi_supervision_head import BaseMultiSupervisionHead
from ..builder import HEADS


class CSAM(nn.Module):
    """
    Compact Spatial Attention Module
    """

    def __init__(self, channels):
        super(CSAM, self).__init__()

        mid_channels = 4
        self.relu1 = nn.ReLU()
        self.conv1 = nn.Conv2d(channels, mid_channels, kernel_size=1, padding=0)
        self.conv2 = nn.Conv2d(mid_channels, 1, kernel_size=3, padding=1, bias=False)
        self.sigmoid = nn.Sigmoid()
        nn.init.constant_(self.conv1.bias, 0)

    def forward(self, x):
        y = self.relu1(x)
        y = self.conv1(y)
        y = self.conv2(y)
        y = self.sigmoid(y)

        return x * y


class CDCM(nn.Module):
    """
    Compact Dilation Convolution based Module
    """

    def __init__(self, in_channels, out_channels):
        super(CDCM, self).__init__()

        self.relu1 = nn.ReLU()
        self.conv1 = nn.Conv2d(in_channels, out_channels, kernel_size=1, padding=0)
        self.conv2_1 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3, dilation=5, padding=5, bias=False
        )
        self.conv2_2 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3, dilation=7, padding=7, bias=False
        )
        self.conv2_3 = nn.Conv2d(
            out_channels, out_channels, kernel_size=3, dilation=9, padding=9, bias=False
        )
        self.conv2_4 = nn.Conv2d(
            out_channels,
            out_channels,
            kernel_size=3,
            dilation=11,
            padding=11,
            bias=False,
        )
        nn.init.constant_(self.conv1.bias, 0)

    def forward(self, x):
        x = self.relu1(x)
        x = self.conv1(x)
        x1 = self.conv2_1(x)
        x2 = self.conv2_2(x)
        x3 = self.conv2_3(x)
        x4 = self.conv2_4(x)
        return x1 + x2 + x3 + x4


class MapReduce(nn.Module):
    """
    Reduce feature maps into a single edge map
    """

    def __init__(self, channels):
        super(MapReduce, self).__init__()
        self.conv = nn.Conv2d(channels, 1, kernel_size=1, padding=0)
        nn.init.constant_(self.conv.bias, 0)

    def forward(self, x):
        return self.conv(x)


@HEADS.register_module()
class PiDiHead(BaseMultiSupervisionHead):
    def __init__(
        self,
        dil=None,
        sa=False,
        edge_key="fuse",
        log_edge_keys=("fuse", "side4"),
        binary_keys=("side1", "side2", "side3", "side4", "fuse"),
        loss_binary=dict(type="ConsensusBinaryEdgeLoss", loss_weight=1.0),
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            binary_keys=binary_keys,
            loss_binary=loss_binary,
            loss_multilabel=None,
            **kwargs,
        )

        # Tiny: dil=8
        # Small: dil=12
        # Normal: dil=24

        self.sa = sa
        if dil is not None:
            assert isinstance(dil, int), "dil should be an int"
        self.dil = dil

        self.conv_reduces = nn.ModuleList()
        if self.sa and self.dil is not None:
            self.attentions = nn.ModuleList()
            self.dilations = nn.ModuleList()
            for i in range(4):
                self.dilations.append(CDCM(self.in_channels[i], self.dil))
                self.attentions.append(CSAM(self.dil))
                self.conv_reduces.append(MapReduce(self.dil))
        elif self.sa:
            self.attentions = nn.ModuleList()
            for i in range(4):
                self.attentions.append(CSAM(self.in_channels[i]))
                self.conv_reduces.append(MapReduce(self.in_channels[i]))
        elif self.dil is not None:
            self.dilations = nn.ModuleList()
            for i in range(4):
                self.dilations.append(CDCM(self.in_channels[i], self.dil))
                self.conv_reduces.append(MapReduce(self.dil))
        else:
            for i in range(4):
                self.conv_reduces.append(MapReduce(self.in_channels[i]))

        self.classifier = nn.Conv2d(4, 1, kernel_size=1)  # has bias
        nn.init.constant_(self.classifier.weight, 0.25)
        nn.init.constant_(self.classifier.bias, 0)

    def forward(self, inputs):
        # [layer1, layer2, layer3, layer4, input_image]
        x = [i for i in inputs]
        assert isinstance(x, list)
        assert len(x) == 5

        img = x.pop(-1)
        bs, c, h, w = img.shape
        resize_to = (h, w)  # TODO: might be too large

        assert len(x) == 4

        x_fuses = []
        if self.sa and self.dil is not None:
            for i, xi in enumerate(x):
                x_fuses.append(self.attentions[i](self.dilations[i](xi)))
        elif self.sa:
            for i, xi in enumerate(x):
                x_fuses.append(self.attentions[i](xi))
        elif self.dil is not None:
            for i, xi in enumerate(x):
                x_fuses.append(self.dilations[i](xi))
        else:
            x_fuses = x

        e1 = self.conv_reduces[0](x_fuses[0])
        e1 = resize(e1, resize_to, mode="bilinear", align_corners=False)

        e2 = self.conv_reduces[1](x_fuses[1])
        e2 = resize(e2, resize_to, mode="bilinear", align_corners=False)

        e3 = self.conv_reduces[2](x_fuses[2])
        e3 = resize(e3, resize_to, mode="bilinear", align_corners=False)

        e4 = self.conv_reduces[3](x_fuses[3])
        e4 = resize(e4, resize_to, mode="bilinear", align_corners=False)

        outputs = [e1, e2, e3, e4]

        fuse = self.classifier(torch.cat(outputs, dim=1))

        return dict(
            side1=e1,
            side2=e2,
            side3=e3,
            side4=e4,
            fuse=fuse,
        )

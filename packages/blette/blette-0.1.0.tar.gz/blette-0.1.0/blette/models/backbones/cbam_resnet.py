#!/usr/bin/env python3

import torch.utils.checkpoint as cp

from mmseg.models.backbones.resnet import (
    BasicBlock as MMSEG_BasicBlock,
    Bottleneck as MMSEG_Bottleneck,
)

from .resnet import ResNet
from ..builder import BACKBONES
from ..utils.attention_modules import ChannelAttention, SpatialAttention


class CBAMBasicBlock(MMSEG_BasicBlock):
    def __init__(self, planes, **kwargs):
        super().__init__(planes=planes, **kwargs)

        self.ca = ChannelAttention(planes)
        self.sa = SpatialAttention()

    def forward(self, x):
        def _inner_forward(x):
            identity = x

            out = self.conv1(x)
            out = self.norm1(out)
            out = self.relu(out)

            out = self.conv2(out)
            out = self.norm2(out)

            # attentions
            out = self.ca(out) * out
            out = self.sa(out) * out

            if self.downsample is not None:
                identity = self.downsample(x)

            out += identity

            return out

        if self.with_cp and x.requires_grad:
            out = cp.checkpoint(_inner_forward, x)
        else:
            out = _inner_forward(x)

        out = self.relu(out)

        return out


class CBAMBottleneck(MMSEG_Bottleneck):
    def __init__(self, planes, **kwargs):
        super().__init__(planes=planes, **kwargs)

        self.ca = ChannelAttention(planes * self.expansion)
        self.sa = SpatialAttention()

    def forward(self, x):
        """Forward function."""

        def _inner_forward(x):
            identity = x

            out = self.conv1(x)
            out = self.norm1(out)
            out = self.relu(out)

            if self.with_plugins:
                out = self.forward_plugin(out, self.after_conv1_plugin_names)

            out = self.conv2(out)
            out = self.norm2(out)
            out = self.relu(out)

            if self.with_plugins:
                out = self.forward_plugin(out, self.after_conv2_plugin_names)

            out = self.conv3(out)
            out = self.norm3(out)

            if self.with_plugins:
                out = self.forward_plugin(out, self.after_conv3_plugin_names)

            # attentions
            out = self.ca(out) * out
            out = self.sa(out) * out

            if self.downsample is not None:
                identity = self.downsample(x)

            out += identity

            return out

        if self.with_cp and x.requires_grad:
            out = cp.checkpoint(_inner_forward, x)
        else:
            out = _inner_forward(x)

        out = self.relu(out)

        return out


@BACKBONES.register_module(force=True)
class CBAMResNet(ResNet):
    arch_settings = {
        18: (CBAMBasicBlock, (2, 2, 2, 2)),
        34: (CBAMBasicBlock, (3, 4, 6, 3)),
        50: (CBAMBottleneck, (3, 4, 6, 3)),
        101: (CBAMBottleneck, (3, 4, 23, 3)),
        152: (CBAMBottleneck, (3, 8, 36, 3)),
    }


@BACKBONES.register_module()
class CBAMResNetV1c(CBAMResNet):
    def __init__(self, **kwargs):
        super(CBAMResNetV1c, self).__init__(deep_stem=True, avg_down=False, **kwargs)


@BACKBONES.register_module()
class CBAMResNetV1d(CBAMResNet):
    def __init__(self, **kwargs):
        super(CBAMResNetV1d, self).__init__(deep_stem=True, avg_down=True, **kwargs)

#!/usr/bin/env python3

"""HED

https://github.com/s9xie/hed
"""

import torch
import torch.nn as nn

from mmcv.cnn import ConvModule
from mmseg.ops import resize

from .multi_supervision_head import BaseMultiSupervisionHead
from ..builder import HEADS


class HEDSideConv(nn.Module):
    def __init__(
        self,
        in_channels,
        out_channels,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=None,
        interpolation="bilinear",
        align_corners=False,
    ):
        super().__init__()
        self.pre_resize = ConvModule(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=1,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
        )
        self._interp = interpolation
        self._align_corners = align_corners

    def forward(self, x, size):
        x = resize(  # (B, out_channels, H, W)
            self.pre_resize(x),
            size=size,
            mode=self._interp,
            align_corners=self._align_corners,
        )
        return x


@HEADS.register_module()
class HEDHead(BaseMultiSupervisionHead):
    def __init__(
        self,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        binary_keys=("side1", "side2", "side3", "side4", "side5", "fuse"),
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

        _interp = "bilinear"  # nearest

        self.dsn1 = HEDSideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.dsn2 = HEDSideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.dsn3 = HEDSideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.dsn4 = HEDSideConv(
            in_channels=self.in_channels[3],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.dsn5 = HEDSideConv(
            in_channels=self.in_channels[4],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.score_final = ConvModule(
            in_channels=5,
            out_channels=1,
            kernel_size=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=None,
            act_cfg=None,
        )

    def forward(self, inputs):

        # [stem, layer1, layer2, layer3, layer4, input_image]
        x = [i for i in inputs]

        assert isinstance(x, list)
        assert len(x) == 6

        bs, c, h, w = x[-1].shape
        resize_to = (h, w)

        side1 = self.dsn1(x[0], resize_to)  # (B, 1, H, W)
        side2 = self.dsn2(x[1], resize_to)  # (B, 1, H, W)
        side3 = self.dsn3(x[2], resize_to)  # (B, 1, H, W)
        side4 = self.dsn4(x[3], resize_to)  # (B, 1, H, W)
        side5 = self.dsn5(x[4], resize_to)  # (B, 1, H, W)

        fuse_cat = torch.cat((side1, side2, side3, side4, side5), dim=1)
        fuse = self.score_final(fuse_cat)

        return dict(
            side1=side1,
            side2=side2,
            side3=side3,
            side4=side4,
            side5=side5,
            fuse=fuse,
        )

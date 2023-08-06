#!/usr/bin/env python3

"""
Attentive DDS

Adding CBAM attention in the basic resblocks
"""

import torch.nn as nn

from .multi_supervision_head import BaseMultiSupervisionHead
from ..builder import HEADS

from ..backbones.cbam_resnet import CBAMBasicBlock
from ..utils import BasicBlockSideConv, SideConv
from ..utils.fusion_layers import GroupedConvFuseSide4

from mmcv.cnn import ContextBlock


class AttBlockSideConv(BasicBlockSideConv):
    """Attentive Basic Block using CBAM."""

    def __init__(
        self,
        in_channels,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
        **kwargs,
    ):
        super().__init__(
            in_channels=in_channels,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
            **kwargs,
        )
        self.att = ContextBlock(
            in_channels=in_channels,
            ratio=1 / 4,
            pooling_type="att",
            fusion_types=("channel_add",),
        )

    def forward(self, x, size):
        x = self.block(x)
        x = self.att(x)
        x = self.side_conv(x, size)
        return x


class CBAMBasicBlockSideConv(nn.Module):
    """Attentive Basic Block using CBAM."""

    def __init__(
        self,
        in_channels,
        out_channels,
        num_blocks=2,
        dilations=None,
        conv_cfg=None,
        norm_cfg=None,
        bias=False,
        act_cfg=dict(type="ReLU"),
        interpolation="bilinear",
        align_corners=False,
    ):
        super().__init__()

        assert num_blocks > 0
        if dilations is None:
            # default is 1
            dilations = tuple([1] * num_blocks)
        assert num_blocks == len(dilations)
        modules = []
        for d in dilations:
            modules.append(
                CBAMBasicBlock(
                    inplanes=in_channels,
                    planes=in_channels,
                    stride=1,
                    dilation=d,
                    downsample=None,
                    conv_cfg=conv_cfg,
                    norm_cfg=norm_cfg,
                )
            )
        self.block = nn.Sequential(*modules)
        self.side_conv = SideConv(
            in_channels=in_channels,
            out_channels=out_channels,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            bias=bias,
            act_cfg=act_cfg,
            interpolation=interpolation,
            align_corners=align_corners,
        )

    def forward(self, x, size):
        x = self.block(x)
        x = self.side_conv(x, size)
        return x


@HEADS.register_module()
class ADDSHead(BaseMultiSupervisionHead):
    def __init__(
        self,
        num_blocks=2,
        dilations=None,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        binary_keys=("side1", "side2", "side3"),
        multilabel_keys=("side4", "side5", "fuse"),
        loss_binary=dict(type="BinaryEdgeLoss", loss_weight=1.0),
        loss_multilabel=dict(type="MultiLabelEdgeLoss", loss_weight=1.0),
        **kwargs,
    ):
        super().__init__(
            input_transform="multiple_select",
            edge_key=edge_key,
            log_edge_keys=log_edge_keys,
            binary_keys=binary_keys,
            multilabel_keys=multilabel_keys,
            loss_binary=loss_binary,
            loss_multilabel=loss_multilabel,
            **kwargs,
        )

        _interp = "bilinear"  # nearest
        _bias = True

        # Sides 1, 2, 3, 4, 5
        self.side1 = AttBlockSideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            num_blocks=num_blocks,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side2 = AttBlockSideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            num_blocks=num_blocks,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side3 = AttBlockSideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            num_blocks=num_blocks,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side4 = AttBlockSideConv(
            in_channels=self.in_channels[3],
            out_channels=self.num_classes,
            num_blocks=num_blocks,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5 = AttBlockSideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            num_blocks=num_blocks,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )

        self.fuse = GroupedConvFuseSide4(
            num_classes=self.num_classes,
            num_sides=5,
            conv_cfg=self.conv_cfg,
        )

    def forward(self, inputs):

        # [stem, layer1, layer2, layer3, layer4, input_image]
        x = [i for i in inputs]

        assert isinstance(x, list)
        assert len(x) == 6

        bs, c, h, w = x[-1].shape
        resize_to = (h, w)  # TODO: might be too large

        side1 = self.side1(x[0], resize_to)  # (B, 1, H, W)
        side2 = self.side2(x[1], resize_to)  # (B, 1, H, W)
        side3 = self.side3(x[2], resize_to)  # (B, 1, H, W)
        side4 = self.side4(x[3], resize_to)  # (B, 1, H, W)
        side5 = self.side5(x[4], resize_to)  # (B, 19, H, W)

        fuse = self.fuse([side1, side2, side3, side4, side5])

        return dict(
            fuse=fuse,
            side5=side5,
            side4=side4,
            side3=side3,
            side2=side2,
            side1=side1,
        )

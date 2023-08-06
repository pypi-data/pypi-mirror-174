#!/usr/bin/env python3

"""DDS (Deep Diverse Supervision)

https://arxiv.org/pdf/1804.02864.pdf
"""

from .multi_supervision_head import BaseMultiSupervisionHead
from ..builder import HEADS
from ..utils import BasicBlockSideConv  # , GroupedConvFuse
from ..utils.fusion_layers import GroupedConvFuseSide4


@HEADS.register_module()
class DDSHead(BaseMultiSupervisionHead):
    def __init__(
        self,
        num_blocks=2,
        dilations=None,
        side_resize_index=-1,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5", "side4"),
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

        self.side_resize_index = side_resize_index

        _interp = "bilinear"  # nearest
        _bias = True

        # Sides 1, 2, 3, 4, 5
        self.side1 = BasicBlockSideConv(
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
        self.side2 = BasicBlockSideConv(
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
        self.side3 = BasicBlockSideConv(
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
        self.side4 = BasicBlockSideConv(
            in_channels=self.in_channels[3],
            out_channels=self.num_classes,  # original: 1
            num_blocks=num_blocks,
            dilations=dilations,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5 = BasicBlockSideConv(
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

        # self.fuse = GroupedConvFuse(
        #     num_classes=self.num_classes,
        #     num_sides=5,
        #     conv_cfg=self.conv_cfg,
        # )
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

        bs, c, h, w = x[self.side_resize_index].shape
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

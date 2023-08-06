#!/usr/bin/env python3

"""Implementation of DFF

https://github.com/Lavender105/DFF/blob/master/exps/models/dff.py
"""

from .multi_supervision_head import BaseMultiSupervisionHead
from ..builder import HEADS
from ..utils import LocationAdaptiveLearner, SideConv, OGSideConv


@HEADS.register_module()
class DFFHead(BaseMultiSupervisionHead):
    def __init__(
        self,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        binary_keys=[],
        multilabel_keys=("fuse", "side5"),
        loss_binary=None,
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
        _bias = True  # turn on?

        # Sides 1, 2, 3, 5 and Side 5 Weight
        self.side1 = SideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side2 = SideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side3 = SideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5 = SideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )
        self.side5_w = SideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes * 4,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            bias=_bias,  # might not need?
            act_cfg=self.act_cfg,
            interpolation=_interp,
            align_corners=self.align_corners,
        )

        self.ada_learner = LocationAdaptiveLearner(
            in_channels=self.num_classes * 4,
            out_channels=self.num_classes * 4,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
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
        side5 = self.side5(x[4], resize_to)  # (B, 19, H, W)
        side5_w = self.side5_w(x[4], resize_to)  # (B, 19*4, H, W)

        fuse = self.ada_learner([side1, side2, side3, side5, side5_w])

        return dict(fuse=fuse, side5=side5)


@HEADS.register_module()
class OGDFFHead(BaseMultiSupervisionHead):
    def __init__(
        self,
        edge_key="fuse",
        log_edge_keys=("fuse", "side5"),
        binary_keys=[],
        multilabel_keys=("fuse", "side5"),
        loss_binary=None,
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

        # Sides 1, 2, 3, 5 and Side 5 Weight
        self.side1 = OGSideConv(
            in_channels=self.in_channels[0],
            out_channels=1,
            rate=1,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.side2 = OGSideConv(
            in_channels=self.in_channels[1],
            out_channels=1,
            rate=4,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.side3 = OGSideConv(
            in_channels=self.in_channels[2],
            out_channels=1,
            rate=8,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.side5 = OGSideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes,
            rate=16,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )
        self.side5_w = OGSideConv(
            in_channels=self.in_channels[4],
            out_channels=self.num_classes * 4,
            rate=16,
            bias=True,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
        )

        self.ada_learner = LocationAdaptiveLearner(
            in_channels=self.num_classes * 4,
            out_channels=self.num_classes * 4,
            conv_cfg=self.conv_cfg,
            norm_cfg=self.norm_cfg,
            act_cfg=self.act_cfg,
            bias=False,
        )

    def forward(self, inputs):

        # [stem, layer1, layer2, layer3, layer4, input_image]
        x = [i for i in inputs]

        assert isinstance(x, list)
        assert len(x) == 6

        side1 = self.side1(x[0])  # (B, 1, H, W)
        side2 = self.side2(x[1])  # (B, 1, H, W)
        side3 = self.side3(x[2])  # (B, 1, H, W)
        side5 = self.side5(x[4])  # (B, 19, H, W)
        side5_w = self.side5_w(x[4])  # (B, 19*4, H, W)

        fuse = self.ada_learner([side1, side2, side3, side5, side5_w])

        return dict(fuse=fuse, side5=side5)

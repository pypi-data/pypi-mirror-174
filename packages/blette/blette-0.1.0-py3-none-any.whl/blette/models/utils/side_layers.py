#!/usr/bin/env python3

import torch.nn as nn

from mmcv.cnn import ConvModule
from mmseg.ops import resize
from mmseg.models.backbones.resnet import BasicBlock


class OGSideConv(nn.Module):
    """Original Side Upsample

    Weird choices in the original paper:
    - no activations after conv when there is a tranpose layer
    - bias + BN
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        rate,
        bias=False,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
    ):
        super().__init__()
        if rate == 1:
            # keeps the same size
            self.side = ConvModule(
                in_channels=in_channels,
                out_channels=out_channels,
                kernel_size=1,
                bias=False,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=None,
            )
        else:
            assert rate % 4 == 0
            self.side = nn.Sequential(
                ConvModule(
                    in_channels=in_channels,
                    out_channels=out_channels,
                    kernel_size=1,
                    bias=bias,
                    conv_cfg=conv_cfg,
                    norm_cfg=norm_cfg,
                    act_cfg=None,
                ),
                nn.ConvTranspose2d(
                    in_channels=out_channels,
                    out_channels=out_channels,
                    kernel_size=rate,
                    stride=rate // 2,
                    padding=rate // 4,
                    bias=False,
                ),
            )

    def forward(self, x):
        return self.side(x)


class SideConv(nn.Module):
    """'Improved' Basic Side Convolution

    instead of deconv, we use
    upsample -> 3x3conv

    https://distill.pub/2016/deconv-checkerboard/
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        conv_cfg=None,
        norm_cfg=None,
        bias=False,
        act_cfg=dict(type="ReLU"),
        interpolation="bilinear",
        align_corners=False,
    ):
        super().__init__()
        self.conv_reduce = ConvModule(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=1,
            bias=False,  # NOTE: added bias
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
        )
        self.post_resize = nn.Sequential(
            nn.ReflectionPad2d(1),
            ConvModule(
                in_channels=out_channels,
                out_channels=out_channels,
                kernel_size=3,
                stride=1,
                padding=0,
                conv_cfg=conv_cfg,
                norm_cfg=None,  # no bn
                bias=bias,
                act_cfg=None,  # no activation -> edge logit
            ),
        )
        self._interp = interpolation
        self._align_corners = align_corners

    def forward(self, x, size):
        x = resize(  # (B, out_channels, H, W)
            self.conv_reduce(x),
            size=size,
            mode=self._interp,
            align_corners=self._align_corners,
        )
        x = self.post_resize(x)
        return x


class BasicBlockSideConv(nn.Module):
    """Side Convolution with Basic Block

    Better 'information converter'
    """

    def __init__(
        self,
        in_channels,
        out_channels,
        num_blocks=2,
        return_block_output=False,
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
                BasicBlock(
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
        self.return_block_output = return_block_output

    def forward(self, x, size):
        x = self.block(x)
        s = self.side_conv(x, size)
        if self.return_block_output:
            return s, x
        else:
            return s

#!/usr/bin/env python3

"""HED-based VGG

Not flexible: only supports VGG16
"""

import warnings
from collections import OrderedDict

import torch.nn as nn

from mmcv.cnn import ConvModule
from mmcv.runner import BaseModule
from mmcv.utils.parrots_wrapper import _BatchNorm

from ..builder import BACKBONES


def make_vgg_layer(
    in_channels,
    out_channels,
    num_blocks,
    conv_cfg=None,
    norm_cfg=None,
    act_cfg=dict(type="ReLU"),
    dilation=1,
    with_norm=False,
    ceil_mode=False,
):
    layers = []

    for _ in range(num_blocks):
        layer = ConvModule(
            in_channels=in_channels,
            out_channels=out_channels,
            kernel_size=3,
            dilation=dilation,
            padding=dilation,
            bias=True,
            conv_cfg=conv_cfg,
            norm_cfg=norm_cfg,
            act_cfg=act_cfg,
        )
        layers.append(layer)
        in_channels = out_channels
    layers.append(nn.MaxPool2d(kernel_size=2, stride=2, ceil_mode=ceil_mode))

    return layers


@BACKBONES.register_module()
class VGG(BaseModule):
    """VGG backbone.
    Args:
        depth (int): Depth of vgg, from {11, 13, 16, 19}.
        with_norm (bool): Use BatchNorm or not.
        num_stages (int): VGG stages, normally 5.
        dilations (Sequence[int]): Dilation of each stage.
        out_indices (Sequence[int], optional): Output from which stages.
            Default: (0, 1, 2, 3, 4).
        frozen_stages (int): Stages to be frozen (all param fixed). -1 means
            not freezing any parameters.
        norm_eval (bool): Whether to set norm layers to eval mode, namely,
            freeze running stats (mean and var). Note: Effect on Batch Norm
            and its variants only. Default: False.
        ceil_mode (bool): Whether to use ceil_mode of MaxPool. Default: False.
        with_last_pool (bool): Whether to keep the last pooling before
            classifier. Default: True.
    """

    # Parameters to build layers. Each element specifies the number of conv in
    # each stage. For example, VGG11 contains 11 layers with learnable
    # parameters. 11 is computed as 11 = (1 + 1 + 2 + 2 + 2) + 3,
    # where 3 indicates the last three fully-connected layers.
    arch_settings = {
        11: (1, 1, 2, 2, 2),
        13: (2, 2, 2, 2, 2),
        16: (2, 2, 3, 3, 3),
        19: (2, 2, 4, 4, 4),
    }

    grouping = {
        16: [1, 4, 8, 12, 16],
    }

    def __init__(
        self,
        depth,
        num_stages=5,
        dilations=(1, 1, 1, 1, 1),
        out_indices=(0, 1, 2, 3, 4),  # FIXME: not being used
        frozen_stages=-1,
        conv_cfg=None,
        norm_cfg=None,
        act_cfg=dict(type="ReLU"),
        norm_eval=False,
        ceil_mode=False,
        with_last_pool=True,
        pretrained=None,
        init_cfg=[
            dict(type="Kaiming", layer=["Conv2d"]),
            dict(type="Constant", val=1.0, layer=["_BatchNorm"]),
            dict(type="Normal", std=0.01, layer=["Linear"]),
        ],
    ):
        assert depth == 16
        super(VGG, self).__init__(init_cfg=init_cfg)
        if depth not in self.arch_settings:
            raise KeyError(f"invalid depth {depth} for vgg")
        self.depth = depth

        self.pretrained = pretrained
        if isinstance(pretrained, str):
            warnings.warn(
                "DeprecationWarning: pretrained is a deprecated, "
                'please use "init_cfg" instead'
            )
            self.init_cfg = dict(type="Pretrained", checkpoint=pretrained)

        # For now, we return activations
        self.capture_key = ".activate"
        grouping = self.grouping[self.depth]
        self.capture_keys = [str(k) + self.capture_key for k in grouping]

        assert num_stages >= 1 and num_stages <= 5
        stage_blocks = self.arch_settings[depth]
        self.stage_blocks = stage_blocks[:num_stages]
        assert len(dilations) == num_stages

        self.frozen_stages = frozen_stages
        self.norm_eval = norm_eval
        with_norm = norm_cfg is not None

        assert max(out_indices) <= num_stages
        self.out_indices = out_indices

        self.in_channels = 3
        start_idx = 0
        vgg_layers = []
        self.range_sub_modules = []
        for i, num_blocks in enumerate(self.stage_blocks):
            num_modules = num_blocks + 1
            end_idx = start_idx + num_modules
            dilation = dilations[i]
            out_channels = 64 * 2**i if i < 4 else 512
            vgg_layer = make_vgg_layer(
                self.in_channels,
                out_channels,
                num_blocks,
                conv_cfg=conv_cfg,
                norm_cfg=norm_cfg,
                act_cfg=act_cfg,
                dilation=dilation,
                with_norm=with_norm,
                ceil_mode=ceil_mode,
            )
            vgg_layers.extend(vgg_layer)
            self.in_channels = out_channels
            self.range_sub_modules.append([start_idx, end_idx])
            start_idx = end_idx
        if not with_last_pool:
            vgg_layers.pop(-1)
            self.range_sub_modules[-1][1] -= 1
        self.module_name = "features"
        self.add_module(self.module_name, nn.Sequential(*vgg_layers))

    def forward(self, x):
        outs = []

        def _forward_hook():
            def hook(module, input, output):
                outs.append(output)

            return hook

        vgg_layers = getattr(self, self.module_name)

        fhooks = []
        for name, layer in vgg_layers.named_modules():
            if name in self.capture_keys:
                hook = layer.register_forward_hook(_forward_hook())
                fhooks.append(hook)

        for i in range(len(self.stage_blocks)):
            for j in range(*self.range_sub_modules[i]):
                vgg_layer = vgg_layers[j]
                x = vgg_layer(x)
            # if i in self.out_indices:
            #     outs.append(x)

        for hook in fhooks:
            hook.remove()

        assert len(outs) == 5

        return tuple(outs)

    def _freeze_stages(self):
        vgg_layers = getattr(self, self.module_name)
        for i in range(self.frozen_stages):
            for j in range(*self.range_sub_modules[i]):
                m = vgg_layers[j]
                m.eval()
                for param in m.parameters():
                    param.requires_grad = False

    def train(self, mode=True):
        super(VGG, self).train(mode)
        self._freeze_stages()
        if mode and self.norm_eval:
            for m in self.modules():
                # trick: eval have effect on BatchNorm only
                if isinstance(m, _BatchNorm):
                    m.eval()


@BACKBONES.register_module()
class RCFVGG(VGG):
    grouping = {
        16: {
            0: [0, 1],
            1: [3, 4],
            2: [6, 7, 8],
            3: [10, 11, 12],
            4: [14, 15, 16],
        }
    }

    def forward(self, x):
        grouping = self.grouping[self.depth]

        selected_out = OrderedDict()

        def _forward_hook(name):
            def hook(module, input, output):
                selected_out[name] = output

            return hook

        vgg_layers = getattr(self, self.module_name)

        fhooks = []
        for name, layer in vgg_layers.named_modules():
            if self.capture_key in name:
                d = int(name.split(".")[0])
                block_num = None
                for b, ds in grouping.items():
                    if d in ds:
                        block_num = b
                assert block_num is not None

                # HACK: ugly naming
                name = str(block_num) + "_" + str(d)
                hook = layer.register_forward_hook(_forward_hook(name))
                fhooks.append(hook)

        for i in range(len(self.stage_blocks)):
            for j in range(*self.range_sub_modules[i]):
                vgg_layer = vgg_layers[j]
                x = vgg_layer(x)
            # if i in self.out_indices:
            #     outs.append(x)

        for hook in fhooks:
            hook.remove()

        return tuple([selected_out])

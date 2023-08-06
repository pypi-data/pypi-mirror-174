#!/usr/bin/env python3

import os.path as osp

import numpy as np
from PIL import Image

import mmcv
from mmcv.utils import print_log

from blette.utils import get_root_logger
from .builder import DATASETS
from .base_dataset import BaseBinaryDataset
from .pipelines import Compose, LoadEdges


class LoadBSDS500(LoadEdges):
    def __init__(
        self,
        threshold=0.3,
        format=False,
        **kwargs,
    ):
        super().__init__(
            binary=True,
            **kwargs,
        )
        self.threshold = threshold
        self.format = format

    def _load_binary(self, filename):
        edge = Image.open(filename).convert("L")
        edge = np.array(edge).astype(np.uint8)

        if self.format:
            edge = edge / 255
            edge[edge >= self.threshold] = 1
            edge[np.logical_and(edge < self.threshold, edge > 0)] = 255
            edge = edge.astype(np.uint8)

        return edge


@DATASETS.register_module()
class BSDS500Dataset(BaseBinaryDataset):
    def __init__(
        self,
        img_suffix=".jpg",
        edge_dir=None,
        edge_map_suffix=".png",
        gt_loader_cfg=None,
        **kwargs,
    ):
        super(BSDS500Dataset, self).__init__(
            img_suffix=img_suffix,
            **kwargs,
        )
        assert edge_dir is not None, f"ERR: edge_dir is not valid: {edge_dir}"
        self.edge_dir = edge_dir
        self.edge_map_suffix = edge_map_suffix

        if gt_loader_cfg is None:
            gt_loader_cfg = dict(format=True)
        else:
            gt_loader_cfg = dict(
                format=True,
                **gt_loader_cfg,
            )
        self.gt_loader = Compose([LoadBSDS500(**gt_loader_cfg)])

        # join paths if data_root is specified
        if self.data_root is not None:
            if not (self.edge_dir is None or osp.isabs(self.edge_dir)):
                self.edge_dir = osp.join(self.data_root, self.edge_dir)

        # load annotations
        assert self.edge_dir is not None
        self.img_infos = self.load_annotations(
            img_dir=self.img_dir,
            img_suffix=self.img_suffix,
            edge_map_suffix=self.edge_map_suffix,
            split=self.split,
        )

    def load_annotations(
        self,
        img_dir,
        img_suffix,
        edge_map_suffix,
        split,
    ):
        img_infos = []
        if split is not None:
            with open(split) as f:
                for line in f:
                    img_name = line.strip()
                    img_info = dict(filename=img_name + img_suffix)
                    edge_map = img_name + edge_map_suffix
                    img_info["ann"] = dict(edge_map=edge_map)
                    img_infos.append(img_info)
        else:
            for img in mmcv.scandir(img_dir, img_suffix, recursive=True):
                img_info = dict(filename=img)
                edge_map = img.replace(img_suffix, edge_map_suffix)
                img_info["ann"] = dict(edge_map=edge_map)
                img_infos.append(img_info)
            img_infos = sorted(img_infos, key=lambda x: x["filename"])

        print_log(f"Loaded {len(img_infos)} images", logger=get_root_logger())
        return img_infos

    def pre_pipeline(self, results):
        results["edge_prefix"] = self.edge_dir

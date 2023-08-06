#!/usr/bin/env python3

"""Customized WandbHook

Differences:
- removed `commit` arg since I didn't want to commit training step when there could be
  validation logs on the same step
"""

import os.path as osp
from typing import Dict, Optional, Union

import mmcv
from mmcv.runner import HOOKS
from mmcv.runner.dist_utils import master_only

from .base_logger import LoggerHook


@HOOKS.register_module()
class BasicWandbHook(LoggerHook):
    def __init__(
        self,
        init_kwargs: Optional[Dict] = None,
        interval: int = 50,
        ignore_last: bool = True,
        reset_flag: bool = False,
        by_epoch: bool = True,
        log_artifact: bool = True,
        out_suffix: Union[str, tuple] = (".log.json", ".log", ".py"),
    ):
        super().__init__(interval, ignore_last, reset_flag, by_epoch)
        self.import_wandb()
        self.init_kwargs = init_kwargs
        self.log_artifact = log_artifact
        self.out_suffix = out_suffix

    def import_wandb(self) -> None:
        try:
            import wandb
        except ImportError:
            raise ImportError('Please run "pip install wandb" to install wandb')
        self.wandb = wandb

    @master_only
    def before_run(self, runner) -> None:
        super().before_run(runner)
        if self.wandb is None:
            self.import_wandb()
        if self.init_kwargs:
            self.wandb.init(**self.init_kwargs)  # type: ignore
        else:
            self.wandb.init()  # type: ignore

    @master_only
    def log(self, runner) -> None:
        tags = self.get_loggable_tags(runner)
        if tags:
            self.wandb.log(tags, step=self.get_iter(runner))

    @master_only
    def after_run(self, runner) -> None:
        if self.log_artifact:
            wandb_artifact = self.wandb.Artifact(name="artifacts", type="model")
            for filename in mmcv.scandir(runner.work_dir, self.out_suffix, True):
                local_filepath = osp.join(runner.work_dir, filename)
                wandb_artifact.add_file(local_filepath)
            self.wandb.log_artifact(wandb_artifact)
        self.wandb.join()

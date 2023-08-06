#!/usr/bin/env python3

import os.path as osp
import warnings

import torch.distributed as dist
from torch.nn.modules.batchnorm import _BatchNorm

from mmcv.runner import DistEvalHook as _DistEvalHook
from mmcv.runner import EvalHook as _EvalHook


class EvalHook(_EvalHook):
    greater_keys = ["mIoU", "mAcc", "aAcc"]

    def __init__(
        self, *args, by_epoch=False, efficient_test=False, pre_eval=False, **kwargs
    ):
        super().__init__(*args, by_epoch=by_epoch, **kwargs)
        self.pre_eval = pre_eval
        if efficient_test:
            warnings.warn(
                "DeprecationWarning: ``efficient_test`` for evaluation hook "
                "is deprecated, the evaluation hook is CPU memory friendly "
                "with ``pre_eval=True`` as argument for ``single_gpu_test()`` "
                "function"
            )

    def _do_evaluate(self, runner):
        """perform evaluation and save ckpt."""
        if not self._should_evaluate(runner):
            return

        from blette.apis import single_gpu_test

        results = single_gpu_test(runner.model, self.dataloader, pre_eval=self.pre_eval)
        runner.log_buffer.clear()
        runner.log_buffer.output["eval_iter_num"] = len(self.dataloader)
        key_score = self.evaluate(runner, results)
        if self.save_best:
            self._save_ckpt(runner, key_score)

    def evaluate(self, runner, results):
        """Evaluate the results.
        Args:
            runner (:obj:`mmcv.Runner`): The underlined training runner.
            results (list): Output results.
        """
        eval_res = self.dataloader.dataset.evaluate(
            results, logger=runner.logger, **self.eval_kwargs
        )

        for name, val in eval_res.items():
            runner.log_buffer.output[name] = val
        runner.log_buffer.mode = "val"  # patch
        runner.log_buffer.ready = True

        if self.save_best is not None:
            # If the performance of model is pool, the `eval_res` may be an
            # empty dict and it will raise exception when `self.save_best` is
            # not None. More details at
            # https://github.com/open-mmlab/mmdetection/issues/6265.
            if not eval_res:
                warnings.warn(
                    "Since `eval_res` is an empty dict, the behavior to save "
                    "the best checkpoint will be skipped in this evaluation."
                )
                return None

            if self.key_indicator == "auto":
                # infer from eval_results
                self._init_rule(self.rule, list(eval_res.keys())[0])
            return eval_res[self.key_indicator]

        return None


class DistEvalHook(_DistEvalHook):

    greater_keys = ["mIoU", "mAcc", "aAcc"]

    def __init__(
        self, *args, by_epoch=False, efficient_test=False, pre_eval=False, **kwargs
    ):
        super().__init__(*args, by_epoch=by_epoch, **kwargs)
        self.pre_eval = pre_eval
        if efficient_test:
            warnings.warn(
                "DeprecationWarning: ``efficient_test`` for evaluation hook "
                "is deprecated, the evaluation hook is CPU memory friendly "
                "with ``pre_eval=True`` as argument for ``multi_gpu_test()`` "
                "function"
            )

    def _do_evaluate(self, runner):
        """perform evaluation and save ckpt."""
        # Synchronization of BatchNorm's buffer (running_mean
        # and running_var) is not supported in the DDP of pytorch,
        # which may cause the inconsistent performance of models in
        # different ranks, so we broadcast BatchNorm's buffers
        # of rank 0 to other ranks to avoid this.
        if self.broadcast_bn_buffer:
            model = runner.model
            for name, module in model.named_modules():
                if isinstance(module, _BatchNorm) and module.track_running_stats:
                    dist.broadcast(module.running_var, 0)
                    dist.broadcast(module.running_mean, 0)

        if not self._should_evaluate(runner):
            return

        tmpdir = self.tmpdir
        if tmpdir is None:
            tmpdir = osp.join(runner.work_dir, ".eval_hook")

        from blette.apis import multi_gpu_test

        results = multi_gpu_test(
            runner.model,
            self.dataloader,
            pre_eval=self.pre_eval,
            tmpdir=tmpdir,
            gpu_collect=self.gpu_collect,
        )

        runner.log_buffer.clear()

        if runner.rank == 0:
            print("\n")
            runner.log_buffer.output["eval_iter_num"] = len(self.dataloader)
            key_score = self.evaluate(runner, results)

            if self.save_best:
                self._save_ckpt(runner, key_score)

    def evaluate(self, runner, results):
        """Evaluate the results.
        Args:
            runner (:obj:`mmcv.Runner`): The underlined training runner.
            results (list): Output results.
        """
        eval_res = self.dataloader.dataset.evaluate(
            results, logger=runner.logger, **self.eval_kwargs
        )

        for name, val in eval_res.items():
            runner.log_buffer.output[name] = val
        runner.log_buffer.mode = "val"  # patch
        runner.log_buffer.ready = True

        if self.save_best is not None:
            # If the performance of model is pool, the `eval_res` may be an
            # empty dict and it will raise exception when `self.save_best` is
            # not None. More details at
            # https://github.com/open-mmlab/mmdetection/issues/6265.
            if not eval_res:
                warnings.warn(
                    "Since `eval_res` is an empty dict, the behavior to save "
                    "the best checkpoint will be skipped in this evaluation."
                )
                return None

            if self.key_indicator == "auto":
                # infer from eval_results
                self._init_rule(self.rule, list(eval_res.keys())[0])
            return eval_res[self.key_indicator]

        return None

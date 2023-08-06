from typing import Iterable, List, Union, Tuple

from attr import define, field
from pytorch_lightning import LightningModule
from pytorch_lightning.callbacks.callback import Callback
from pytorch_lightning.utilities.model_summary import DeepSpeedSummary
from pytorch_lightning.utilities.model_summary import ModelSummary as Summary
from pytorch_lightning.utilities.model_summary import summarize
from pytorch_lightning.utilities.model_summary.model_summary import _format_summary_table
from torch.nn import Module, ModuleDict
from torch.nn.modules.batchnorm import _BatchNorm


@define
class FreezePlugin:
    model: LightningModule = field()

    def __call__(self, modules: Union[str, Module, Iterable[Union[Module, Iterable]]] = 'backbone',
                 include_bn: bool = True, freeze: bool = True):
        if isinstance(modules, str):
            modules = getattr(self.model, modules)
        if freeze:
            self.freeze(modules, train_bn=include_bn)
        else:
            self.unfreeze(modules)

    @staticmethod
    def flatten_modules(modules: Union[Module, Iterable[Union[Module, Iterable]]]) -> List[Module]:
        """This function is used to flatten a module or an iterable of modules into a list of its leaf modules
        (modules with no children) and parent modules that have parameters directly themselves.

        Args:
            modules: A given module or an iterable of modules

        Returns:
            List of modules
        """
        if isinstance(modules, ModuleDict):
            modules = modules.values()

        if isinstance(modules, Iterable):
            _flatten_modules = []
            for m in modules:
                _flatten_modules.extend(FreezePlugin.flatten_modules(m))

            _modules = iter(_flatten_modules)
        else:
            _modules = modules.modules()

        # Capture all leaf modules as well as parent modules that have parameters directly themselves
        return [m for m in _modules if not list(m.children()) or m._parameters]

    @staticmethod
    def unfreeze(modules: Union[Module, Iterable[Union[Module, Iterable]]]) -> None:
        """Unfreezes the parameters of the provided modules.

        Args:
            modules: A given module or an iterable of modules
        """
        modules = FreezePlugin.flatten_modules(modules)
        for module in modules:
            # recursion could yield duplicate parameters for parent modules w/ parameters so disabling it
            for param in module.parameters(recurse=False):
                param.requires_grad = True

    @staticmethod
    def freeze(modules: Union[Module, Iterable[Union[Module, Iterable]]], train_bn: bool = True) -> None:
        """Freezes the parameters of the provided modules.

        Args:
            modules: A given module or an iterable of modules
            train_bn: If True, leave the BatchNorm layers in training mode

        Returns:
            None
        """
        modules = FreezePlugin.flatten_modules(modules)
        for mod in modules:
            if isinstance(mod, _BatchNorm) and train_bn:
                FreezePlugin.unfreeze(mod)
            else:
                # recursion could yield duplicate parameters for parent modules w/ parameters so disabling it
                for param in mod.parameters(recurse=False):
                    param.requires_grad = False


@define
class SummaryPlugin:

    model: LightningModule = field()
    _max_depth: int = field(default=1)

    def __call__(self, max_depth: int = 1) -> None:
        self._max_depth: int = max_depth
        self.on_fit_start(self.model.fit.trainer, self.model)

    def on_fit_start(self, trainer, pl_module) -> None:
        if not self._max_depth:
            return None

        model_summary = self._summary(trainer, pl_module)
        summary_data = model_summary._get_summary_data()
        total_parameters = model_summary.total_parameters
        trainable_parameters = model_summary.trainable_parameters
        model_size = model_summary.model_size

        if trainer.is_global_zero:
            self.summarize(summary_data, total_parameters, trainable_parameters, model_size)

    def _summary(self, trainer, pl_module) -> Union[DeepSpeedSummary, Summary]:
        from pytorch_lightning.strategies.deepspeed import DeepSpeedStrategy

        if isinstance(trainer.strategy, DeepSpeedStrategy) and trainer.strategy.zero_stage_3:
            return DeepSpeedSummary(pl_module, max_depth=self._max_depth)
        return summarize(pl_module, max_depth=self._max_depth)

    @staticmethod
    def summarize(
            summary_data: List[Tuple[str, List[str]]],
            total_parameters: int,
            trainable_parameters: int,
            model_size: float,
    ) -> None:
        summary_table = _format_summary_table(total_parameters, trainable_parameters, model_size, *summary_data)
        print("\n" + summary_table)

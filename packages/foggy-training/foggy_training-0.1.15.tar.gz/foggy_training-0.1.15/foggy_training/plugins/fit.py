from typing import Union, List

import torch
from attr import field, asdict, define
from datasets import Dataset
from pytorch_lightning import Callback, LightningModule, Trainer
from torch.utils.data import DataLoader

from foggy_training.plugins.utils import prepare_for_model


@define
class DataConfig:
    batch_size: int = 32
    num_workers: int = 6
    shuffle: bool = False

    def cpu(self):
        self.num_workers = 0
        self.batch_size = 32

    def gpu(self):
        self.num_workers = 6
        self.batch_size = 32

    @property
    def as_dict(self):
        return asdict(self)  # noqa


@define
class FitPlugin:

    """
    The FitPlugin allows you to directly train on datasets.
    """

    model: LightningModule = field()
    max_epochs: int = 20
    auto_scale_batch_size: Union[str, bool] = False
    callbacks: List[Callback] = field(factory=lambda: [])
    accelerator: str = 'gpu'
    precision: Union[int, str] = 16
    logger: bool = True
    gradient_clip_val: Union[int, float] = None
    enable_progress_bar: bool = True
    overfit_batches: Union[int, float] = 0.0
    track_grad_norm: Union[int, float, str] = -1
    fast_dev_run: Union[int, bool] = False
    log_every_n_steps: int = 50
    enable_model_summary: bool = True
    num_sanity_val_steps: int = 2
    data_config: DataConfig = field(default=DataConfig())

    def __attrs_post_init__(self):
        if not torch.cuda.is_available():
            self.cpu()
            print('training config set to cpu because no gpu was detected.')

    def cpu(self):
        self.accelerator = 'cpu'
        self.precision = 32
        self.logger = False
        # self.overfit_batches = 3
        self.data_config.cpu()

    def gpu(self):
        self.accelerator = 'gpu'
        self.precision = 16
        self.logger = True
        self.overfit_batches = 0.0
        self.data_config.gpu()

    @property
    def as_dict(self):
        exclude = ['model', 'data_config']
        return asdict(self, filter=lambda attr, value: attr.name not in exclude)  # noqa

    @property
    def trainer(self) -> Trainer:
        return Trainer(**self.as_dict)

    def __call__(self, train_dataset: Dataset, epochs: int = 20, val_dataset: Union[Dataset, float, int] = None):
        train_dataset = prepare_for_model(train_dataset, self.model.task)

        if val_dataset is not None:
            if isinstance(val_dataset, float) or isinstance(val_dataset, int):
                val_dataset = train_dataset.train_test_split(test_size=val_dataset, seed=31)

        self.data_config.shuffle = True
        train_dataset = prepare_for_model(train_dataset, self.model.task)
        train_dataloader = DataLoader(train_dataset, **self.data_config.as_dict)

        if val_dataset is not None:
            val_dataset = prepare_for_model(val_dataset, self.model.task)
            cfg = self.data_config.as_dict
            cfg['shuffle'] = False
            val_dataset = DataLoader(val_dataset, **cfg)

        self.max_epochs = epochs

        self.trainer.fit(self.model, train_dataloaders=train_dataloader, val_dataloaders=val_dataset)

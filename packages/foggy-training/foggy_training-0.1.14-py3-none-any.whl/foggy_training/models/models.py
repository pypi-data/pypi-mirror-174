from functools import singledispatchmethod

from datasets import Dataset, DatasetDict
from torch import nn
from torch.nn.functional import mse_loss, cross_entropy, softmax
from transformers import AutoConfig, AutoModel, AutoTokenizer

from foggy_training.base import LightningExtended, Task, TransformerTask
from foggy_training.plugins.prepare import TokenizePlugin


class LinearRegression(LightningExtended):
    def __init__(self, n_inputs=4):
        super().__init__(loss=mse_loss)
        self.linear = nn.Linear(n_inputs, 1)
        self.lr = 1e-3

    def forward(self, x):
        return self.linear(x)


class SoftmaxClassifier(LightningExtended):
    def __init__(self, n_inputs: int, n_classes: int, task: Task):
        super().__init__(loss=cross_entropy, task=task)
        self.linear = nn.Linear(n_inputs, n_classes)

    def forward(self, x):
        x = x['x']
        x = self.linear(x)
        return softmax(x, dim=-1)


class TransformerModel(LightningExtended):
    def __init__(self, backbone: str, loss: callable, task: TransformerTask):
        super().__init__(loss=loss, task=task)
        config = AutoConfig.from_pretrained(backbone)
        self.backbone = backbone
        self.backbone_ = AutoModel.from_pretrained(backbone, config=config)
        self.tokenize = TokenizePlugin(self)
        self.head = task.build_head(self)

    def forward(self, x: dict):
        x = self.backbone_(input_ids=x["input_ids"], attention_mask=x["attention_mask"])
        x = self.head(x)
        return x

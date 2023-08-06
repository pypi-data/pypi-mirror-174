from torch import nn
from torch.nn.functional import mse_loss, cross_entropy, softmax
from transformers import AutoConfig, AutoModel

from foggy_training.base import LightningExtended, Task, TransformerTask
from foggy_training.plugins.prepare import TokenizePlugin


class SoftmaxClassifier(LightningExtended):
    def __init__(self, n_inputs: int, n_classes: int, task: Task, metrics=None):
        super().__init__(loss=cross_entropy, task=task, metrics=metrics)
        self.linear = nn.Linear(n_inputs, n_classes)

    def forward(self, x):
        x = x['x']
        x = self.linear(x)
        return softmax(x, dim=-1)


class TransformerModel(LightningExtended):
    def __init__(self, backbone: str, loss: callable, task: TransformerTask, metrics=None):
        super().__init__(loss=loss, task=task, metrics=metrics)
        config = AutoConfig.from_pretrained(backbone)
        self.backbone = backbone
        self.backbone_ = AutoModel.from_pretrained(backbone, config=config)
        self.tokenize = TokenizePlugin(self)
        self.head = task.build_head(self)

    def forward(self, x: dict):
        x = self.backbone_(input_ids=x["input_ids"], attention_mask=x["attention_mask"])
        x = self.head(x)
        return x

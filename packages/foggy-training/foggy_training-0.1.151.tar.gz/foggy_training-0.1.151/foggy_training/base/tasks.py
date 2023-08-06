from typing import List, Union

from attr import define, field
from torch import nn


@define
class Task:
    model_inputs: Union[List[str], str] = field(converter=lambda v: v if isinstance(v, list) else [v])
    model_target: str = field()


@define
class MultiOutputRegression(Task):
    pass


@define
class Classification(Task):
    pass


@define
class TransformerTask(Task):
    tokenize_column: str = field()

    def build_head(self, model):
        input_size = model.backbone_.config.hidden_size
        hidden_size = 150
        num_layers = 2
        num_classes = 6

        class LambdaLayer(nn.Module):
            def __init__(self, lambd):
                super(LambdaLayer, self).__init__()
                self.lambd = lambd

            def forward(self, x):
                return self.lambd(x)

        return nn.Sequential(
            LambdaLayer(lambda x: x.last_hidden_state),
            nn.LSTM(input_size=input_size, hidden_size=hidden_size, num_layers=num_layers, batch_first=True),
            LambdaLayer(lambda x: x[0]),
            nn.Linear(hidden_size, hidden_size // 2),
            nn.Flatten(),
            nn.LazyLinear(num_classes)
        )


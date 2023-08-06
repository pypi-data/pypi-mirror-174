import pytorch_lightning as pl
from torch import optim

from foggy_training.base import Task
from foggy_training.plugins.evaluate import EvaluatePlugin
from foggy_training.plugins.fit import FitPlugin
from foggy_training.plugins.freeze import FreezePlugin, SummaryPlugin
from foggy_training.plugins.prediction import PredictPlugin



class LightningExtended(pl.LightningModule):

    """

    The Lightning Extended Modules provides some defaults for training and validation sets. You may do the following:

    ```python
    from foggy_training import models
    x = [[1., 1.], [2., 2.], [3., 3.]]
    y = [1., 2., 3.]
    data = {'x': x, 'y': y}
    model = models.LinearRegression(n_inputs=2)
    model.fit(data, epochs=20)
    ```

    """
    def __init__(self, loss: callable, task: Task):
        super(LightningExtended, self).__init__()
        self.task: Task = task
        self.fit = FitPlugin(self)
        self.predict = PredictPlugin(self)
        self.evaluate = EvaluatePlugin(self)
        self.freeze = FreezePlugin(self)
        self.summary = SummaryPlugin(self)
        self.loss = loss
        self.lr = 1e-3

    def shared_step(self, batch):
        x = {k: batch[k] for k in self.task.model_inputs}
        y = batch.get(self.task.model_target)
        pred = self(x)
        return pred, y

    def training_step(self, batch, batch_idx):
        pred, y = self.shared_step(batch)
        loss = self.loss(pred, y)
        logs = dict(loss=loss)
        self.log_dict(logs, prog_bar=True, on_epoch=True)
        return loss

    def validation_step(self, batch, batch_idx):
        pred, y = self.shared_step(batch)
        loss = self.loss(pred, y)
        logs = dict(val_loss=loss)
        self.log_dict(logs, prog_bar=True, on_epoch=True)

    def predict_step(self, batch, batch_idx, dataloader_idx=0):
        return self.shared_step(batch)[0]

    def configure_optimizers(self):
        return optim.AdamW(filter(lambda p: p.requires_grad, self.parameters()), lr=self.lr)

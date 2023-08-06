from functools import partial

from attr import define, field
from datasets import Dataset
from pytorch_lightning import LightningModule

from foggy_training.plugins.utils import prepare_for_model


@define
class EvaluatePlugin:

    """
    The EvaluatePlugin allows you to directly evaluate on datasets.
    """

    model: LightningModule = field()

    def __call__(self, dataset: Dataset):
        if 'loss' in dataset.features:
            print('dataset has already a feature named loss. Did you run the evaluation previously?')
            return dataset

        prep = prepare_for_model(dataset, self.model.task)
        predicted = self.model.predict(prep, warn_prediction_exists=False)
        n_loss = partial(self.model.loss, reduction='none')
        y = predicted[self.model.task.model_target]
        # y = F.one_hot(predicted[self.model.task.model_target]).double()
        loss_value = n_loss(predicted['predicted'], y).numpy().tolist()
        return dataset.add_column('loss', loss_value)

    def highest_loss_instances(self, dataset: Dataset):
        if 'loss' not in dataset.features:
            dataset = self(dataset)
        dataset.set_format('pd')
        return dataset.sort('loss', reverse=True)

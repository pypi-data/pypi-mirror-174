from functools import partial, singledispatchmethod

from attr import define, field
from datasets import Dataset, DatasetDict
from pytorch_lightning import LightningModule

from foggy_training.plugins.utils import prepare_for_model


@define
class EvaluatePlugin:

    """
    The EvaluatePlugin allows you to directly evaluate on datasets.
    """

    model: LightningModule = field()

    @singledispatchmethod
    def __call__(self, dataset: Dataset):
        if 'loss' in dataset.features:
            print('dataset has already a feature named loss. Did you run the evaluation previously?')
            return dataset

        prep = prepare_for_model(dataset, self.model.task)
        predicted = self.model.predict(prep, warn_prediction_exists=False)
        n_loss = partial(self.model.loss, reduction='none')
        y = predicted[self.model.task.model_target]
        # y = F.one_hot(predicted[self.model.task.model_target]).double()
        loss_value = n_loss(predicted['predicted'], y).numpy()

        if len(loss_value.shape) == 2:
            loss_value = loss_value.sum(axis=-1)
        if len(loss_value.shape) > 2:
            raise ValueError(f'loss has more than 2 dimensions. cannot calculate loss per instance then.')

        loss_value = loss_value.tolist()
        return dataset.add_column('loss', loss_value)

    @__call__.register
    def evaluate_on_dataset_dict(self, dataset: DatasetDict, warn_prediction_exists: bool = True):
        for d in dataset:
            dataset[d] = self(dataset[d], warn_prediction_exists)
        return dataset

    def highest_loss_instances(self, dataset: Dataset):
        if 'loss' not in dataset.features:
            dataset = self(dataset)
        dataset.set_format('pd')
        return dataset.sort('loss', reverse=True)

from functools import singledispatchmethod

from attr import define, field
from datasets import Dataset
from pytorch_lightning import LightningModule
from torch.utils.data import DataLoader
import torch

from foggy_training.plugins.utils import prepare_for_model


@define
class PredictPlugin:
    """
    The FitPlugin allows you to directly train on datasets.
    """

    model: LightningModule = field()

    @singledispatchmethod
    def __call__(self, data, warn_prediction_exists: bool = True):
        raise NotImplementedError(f'No fit method defined for type {type(data)}')

    @__call__.register
    def predict_on_dataset(self, dataset: Dataset, warn_prediction_exists: bool = True):
        if 'predicted' in dataset.features:
            if warn_prediction_exists:
                print(
                    'dataset has already a feature named predicted. '
                    'Did you run the evaluation previously? I skip predictions and take the existent predictions.')
            return dataset

        # disable shuffling for prediction
        config = self.model.fit.data_config.as_dict
        config = {**config, 'shuffle': False}

        # data to DataLoader
        prep = prepare_for_model(dataset, self.model.task)
        dataloader = DataLoader(prep, **config)

        predictions = self.model.fit.trainer.predict(self.model, dataloader)
        predictions = torch.cat(predictions).numpy().tolist()
        dataset = dataset.add_column('predicted', predictions)
        return dataset

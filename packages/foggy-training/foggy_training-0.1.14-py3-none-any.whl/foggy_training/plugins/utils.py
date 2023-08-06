from datasets import Dataset

from foggy_training.base import Task


def prepare_for_model(dataset: Dataset, task: Task):
    inputs = task.model_inputs
    target = task.model_target
    remove = [c for c in dataset.features if c not in inputs + [target]]
    dataset = dataset.remove_columns(remove)
    dataset.set_format('pt')
    return dataset

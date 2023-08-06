from attr import define, field
from datasets import Dataset
from pytorch_lightning import LightningModule
from transformers import AutoTokenizer


@define
class TokenizePlugin:

    model: LightningModule = field()

    def __call__(self, dataset: Dataset, padding='max_length', truncation=True, add_input_length: bool = True):
        tokenizer = AutoTokenizer.from_pretrained(self.model.backbone)
        dataset = dataset.map(
            lambda examples: tokenizer(examples[self.model.task.tokenize_column],
                                       padding=padding, truncation=truncation, return_tensors="np"),
            batched=True, desc='tokenizing'
        )

        self.model.task.model_inputs += tokenizer.model_input_names
        # list(set(...)) to remove duplicates in case the user added input names before
        self.model.task.model_inputs = list(set(self.model.task.model_inputs))

        return dataset

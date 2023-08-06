from functools import singledispatchmethod

from datasets import Dataset, DatasetDict
from transformers import AutoTokenizer


@singledispatchmethod
def analyze_length_of_text(self, dataset: Dataset):
    if 'text_length' in dataset.features:
        print('skip analysis because text_length already exists.')
        return dataset

    tokenizer = AutoTokenizer.from_pretrained(self.backbone)
    tokenized = dataset.map(
        lambda examples: tokenizer(examples[self.task.tokenize_column],
                                   padding=False, truncation=False, return_tensors="np"),
        batched=True, desc='tokenizing'
    )
    length = tokenized.map(lambda x: dict(text_length=len(x['input_ids'])))
    dataset = dataset.add_column('text_length', length['text_length'])
    return dataset


@analyze_length_of_text.register
def _(self, dataset: DatasetDict):
    for d in dataset:
        dataset[d] = self.analyze_length_of_text(dataset[d])
    return dataset



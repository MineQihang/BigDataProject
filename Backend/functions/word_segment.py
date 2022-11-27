from typing import Union,List,Optional
import numpy as np
import torch
from torch.utils.data import (
    DataLoader,
    TensorDataset,
)
from tqdm import tqdm
from transformers import BatchEncoding

# 下游任务 WordSegmenter分词
class WordSegmenter():
    r"""
    使用预训练模型进行中文分词
    """
    def __init__(self,model,tokenizer,device: Union[int, torch.device] = -1)->None:
        self.model = model
        self.tokenizer = tokenizer
        if isinstance(device, torch.device):
            self.device = device
        else:
            self.device = torch.device("cpu" if device < 0 else f"cuda:{device}")

        self.model.to(self.device)

    def __call__(
        self,
        input_text: Union[List[str], List[List[str]]],
        *,
        use_delim: bool = False,
        delim_set: Optional[str] = "，,。：:；;！!？?",
        batch_size: int = 256,
        max_length: Optional[int] = None,
        show_progress: bool = False,
        pin_memory: bool = True,
    ):

        model_max_length = self.tokenizer.model_max_length - 2  # Add [CLS] and [SEP]
        if max_length:
            assert max_length < model_max_length, (
                "Sequence length is longer than the maximum sequence length for this model "
                f"({max_length} > {model_max_length})."
            )
        else:
            max_length = model_max_length

        # Apply delimiter cut
        delim_index = self._find_delim(
            input_text=input_text,
            use_delim=use_delim,
            delim_set=delim_set,
        )

        # Get worded input IDs
        if show_progress:
            input_text = tqdm(input_text, desc="Tokenization")

        input_ids_worded = [
            [self.tokenizer.convert_tokens_to_ids(list(input_word)) for input_word in input_sent] for input_sent in input_text
        ]

        # Flatten input IDs
        (input_ids, index_map,) = self._flatten_input_ids(
            input_ids_worded=input_ids_worded,
            max_length=max_length,
            delim_index=delim_index,
        )

        # Pad and segment input IDs
        (input_ids, attention_mask,) = self._pad_input_ids(
            input_ids=input_ids,
        )

        # Convert input format
        encoded_input = BatchEncoding(
            data=dict(
                input_ids=input_ids,
                attention_mask=attention_mask,
            ),
            tensor_type="pt",
        )

        # Create dataset
        dataset = TensorDataset(*encoded_input.values())
        dataloader = DataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=False,
            drop_last=False,
            pin_memory=pin_memory,
        )
        if show_progress:
            dataloader = tqdm(dataloader, desc="Inference")

        # Call Model
        logits = []
        with torch.no_grad():
            for batch in dataloader:
                batch = tuple(tensor.to(self.device) for tensor in batch)
                (batch_logits,) = self.model(**dict(zip(encoded_input.keys(), batch)), return_dict=False)
                batch_logits = batch_logits.cpu().numpy()[:, 1:, :]  # Remove [CLS]
                logits.append(batch_logits)

        # Call model
        logits = np.concatenate(logits, axis=0)

        return logits, index_map
    @staticmethod
    def _find_delim(
        *,
        input_text,
        use_delim,
        delim_set,
    ):
        if not use_delim:
            return set()

        delim_index = set()
        delim_set = set(delim_set)
        for sent_idx, input_sent in enumerate(input_text):
            for word_idx, input_word in enumerate(input_sent):
                if input_word in delim_set:
                    delim_index.add((sent_idx, word_idx))
        return delim_index
    @staticmethod
    def _flatten_input_ids(
        *,
        input_ids_worded,
        max_length,
        delim_index,
    ):
        input_ids = []
        index_map = []

        input_ids_sent = []
        index_map_sent = []

        for sent_idx, input_ids_worded_sent in enumerate(input_ids_worded):
            for word_idx, word_ids in enumerate(input_ids_worded_sent):
                word_length = len(word_ids)

                if word_length == 0:
                    index_map_sent.append(None)
                    continue

                # Check if sentence segmentation is needed
                if len(input_ids_sent) + word_length > max_length:
                    input_ids.append(input_ids_sent)
                    input_ids_sent = []

                # Insert tokens
                index_map_sent.append(
                    (
                        len(input_ids),  # line index
                        len(input_ids_sent),  # token index
                    )
                )
                input_ids_sent += word_ids

                if (sent_idx, word_idx) in delim_index:
                    input_ids.append(input_ids_sent)
                    input_ids_sent = []

            # End of a sentence
            if input_ids_sent:
                input_ids.append(input_ids_sent)
                input_ids_sent = []
            index_map.append(index_map_sent)
            index_map_sent = []

        return input_ids, index_map

    def _pad_input_ids(
        self,
        *,
        input_ids,
    ):
        max_length = max(map(len, input_ids))

        padded_input_ids = []
        attention_mask = []
        for input_ids_sent in input_ids:
            token_count = len(input_ids_sent)
            pad_count = max_length - token_count
            padded_input_ids.append(
                [self.tokenizer.cls_token_id]
                + input_ids_sent
                + [self.tokenizer.sep_token_id]
                + [self.tokenizer.pad_token_id] * pad_count
            )
            attention_mask.append([1] * (token_count + 2) + [0] * pad_count)  # [CLS] & input & [SEP]  # [PAD]s
        return padded_input_ids, attention_mask

    def segment(self,input_text:str)->List[str]:
        logits,index_map = self.__call__(input_text)
        # Post-process results
        output_text = []
        for sent_data in zip(input_text, index_map):
            output_sent = []
            word = ""
            for input_char, logits_index in zip(*sent_data):
                if logits_index is None:
                    if word:
                        output_sent.append(word)
                    output_sent.append(input_char)
                    word = ""
                else:
                    logits_b, logits_i = logits[logits_index]

                    if logits_b > logits_i:
                        if word:
                            output_sent.append(word)
                        word = input_char
                    else:
                        word += input_char

            if word:
                output_sent.append(word)
            output_text.append(output_sent)

        return output_text
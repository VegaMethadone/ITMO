import os
import json
import torch
from tqdm import tqdm
from transformers import BartTokenizer

articles = []
tags = []


# Инициализация токенизатора BART
tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

# Пример входных текстов
x_train = [
    "This is a positive review.",
    "I really enjoyed this movie!",
    "The product works great.",
    "I had a terrible experience with their customer service.",
    "The quality of the book is poor.",
    "The hotel room was clean and comfortable.",
    # ... Другие примеры текстов ...
]

# Максимальная длина текста после токенизации и паддинга
max_length = 1000

# Преобразование текстов в последовательности токенов и паддинг
input_ids = []
attention_masks = []

for text in tqdm(x_train):
    encoded = tokenizer.encode_plus(
        text,
        max_length=max_length,
        padding='max_length',
        truncation=True,
        return_tensors='pt'
    )
    input_ids.append(encoded['input_ids'].squeeze())
    attention_masks.append(encoded['attention_mask'].squeeze())

# Преобразование в тензоры PyTorch
input_ids = torch.stack(input_ids)
attention_masks = torch.stack(attention_masks)

# Вывод размерности тензоров
print("Input IDs shape:", input_ids.shape)
print("Attention Masks shape:", attention_masks.shape)

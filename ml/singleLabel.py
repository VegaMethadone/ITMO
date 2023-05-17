import torch
from tqdm import tqdm
from transformers import BartForSequenceClassification, BartTokenizer
from torch.utils.data import DataLoader, TensorDataset
from transformers import BartTokenizer

# Подготовка данных
texts = [
    "Это пример первого текста.",
    "Это пример второго текста, который длиннее первого текста."
]
labels = [0, 1]

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')

max_length = 1000

# Преобразование текстов в последовательности токенов и паддинг
input_ids = []
attention_masks = []

for text in tqdm(texts):
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


encoded_inputs = tokenizer(texts, padding=True, truncation=True, return_tensors='pt')
input_ids = encoded_inputs['input_ids']
attention_mask = encoded_inputs['attention_mask']
dataset = TensorDataset(input_ids, attention_mask, torch.tensor(labels))

# Создание модели и оптимизатора
model = BartForSequenceClassification.from_pretrained('facebook/bart-base', num_labels=2)
optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)


# Цикл обучения
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)
train_dataloader = DataLoader(dataset, batch_size=2, shuffle=True)

num_epochs = 10
for epoch in range(num_epochs):
    total_loss = 0
    
    for batch in train_dataloader:
        batch = [item.to(device) for item in batch]
        input_ids, attention_mask, labels = batch
        
        optimizer.zero_grad()
        
        outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
        loss = outputs.loss
        total_loss += loss.item()
        
        loss.backward()
        optimizer.step()
    
    average_loss = total_loss / len(train_dataloader)
    print(f"Epoch {epoch+1}/{num_epochs} - Loss: {average_loss:.4f}")

    


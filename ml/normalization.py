import torch
import os
import json 
import nltk 
import re 
from tqdm import tqdm
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


nltk.download('stopwords')
nltk.download('punkt')

contents = []
tags = []
articles = []


def text_cleaning(text):
    # Приведение к нижнему регистру
    text.lower()
    # Очистка текста от всех ненужных символов
    reg = re.compile('[^а-яА-ЯёЁa-zA-Z ]')
    text = reg.sub('', text)
    stop_words = set(stopwords.words("russian"))
    # Токенизация, избавления от пробелов и стоп-слов
    tokenized_text = [word for word in word_tokenize(text) if word not in stop_words]

    return tokenized_text

def text_cleaning_Bart(text):
    # Приведение к нижнему регистру
    text.lower()
    # Очистка текста от всех ненужных символов
    reg = re.compile('[^а-яА-ЯёЁa-zA-Z ]')
    text = reg.sub('', text)
    stop_words = set(stopwords.words("russian"))
    # Токенизация, избавления от пробелов и стоп-слов

    # Разделение текста на слова
    words = text.split()
    # Фильтрация стоп-слов
    filtered_words = [word for word in words if word.lower() not in stop_words]  
    # Преобразование отфильтрованных слов обратно в текст
    filtered_text = ' '.join(filtered_words)  
    
    return filtered_text
    

def text_earning():
# Создание папки под нормализованные статьи    
    try:
        os.mkdir("normolized_aticles")
        print("Mkdir normolized_aticles")
    except FileExistsError:
        print("File is already exists")

# Создаем список всех статей
    for cursor in tqdm(os.listdir("./articles")):
        articles.append(cursor)

# Обрабатываем каждую стать & записываем в json 
    for text in tqdm(articles):
        with open(f'./articles/{text}', encoding='utf-8') as asset:
            loaded = json.load(asset)

        tmp = text_cleaning_Bart(loaded["content"])

        artile = {
            "article_id": loaded["article_id"],
            "article_name": loaded["article_name"],
            "content": tmp,
            "tags": loaded["tags"]
        }           

        with open(f'./normolized_aticles/article_{loaded["article_id"]}.json', 'w', encoding='utf-8') as f:
            json.dump(artile, f, indent=4, ensure_ascii=False)
            
        
if __name__ == "__main__":
    text_earning()
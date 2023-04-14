import requests
from bs4 import BeautifulSoup
import json
import os
import shutil

def mkdir_own():
    try: 
        shutil.rmtree('./assets')
    except FileNotFoundError:
        pass
    os.mkdir('./assets')



def parse_article():

    with open("links.json") as link:
        data = json.load(link)
    
    i = 1
    os.chdir('./assets')

    for object in data:
        url = f'https://habr.com{object["article_link"]}'
        response = requests.get(url)

        soup = BeautifulSoup(response.content, "html.parser")

        article_text = ""
        for p in soup.find_all("div", class_="article-formatted-body"):
            article_text += p.text.strip()

        data = {f"article{i}": article_text}
        with open(f"article{i}.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        i += 1



def main():
    parse_article()

if __name__ == '__main__':
    main()

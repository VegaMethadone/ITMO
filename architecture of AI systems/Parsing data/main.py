#from pathlib import Path
#import json
#from bs4 import BeautifulSoup
#import requests
#import os
#import shutil
#
#
#def mkdir_own():
#    try: 
#        shutil.rmtree('./assets')
#    except FileNotFoundError:
#        pass
#    os.mkdir('./assets')
#    
#
#def linkCreation():
#    with open("links.json") as link:
#        data  = json.load(link)
#
#    for object in data:
#       tmp = f'https://habr.com{object["article_link"]}'
#       response = requests.get(tmp)
#
#       soup = BeautifulSoup(response.content,  "html.parser")
#       i = 1
#       os.chdir('./assets')
#       for p in soup.find_all("p"):
#           with open(f'article{i}.txt', 'w', encoding='utf-8') as f:
#           
#          
#
#
#def main():
#    mkdir_own()
#    linkCreation()
#
#
#if __name__ == '__main__':
#    main()



# data = {"text": p.text}
#           with open(f'article{i}.json', 'w', encoding='utf-8') as f:
#               json.dump(data, f, ensure_ascii=False, indent=2) 
#           i += 1
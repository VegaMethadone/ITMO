import os
import json

from operator import itemgetter

articles = []
tags = []

for cursor in os.listdir("./normolized_aticles"):
    articles.append(cursor)


for cursor in articles:
    with open(f'normolized_aticles/{cursor}', encoding='utf-8') as asset:
        data = json.load(asset)
    tmp = data["tags"]
    for i in tmp:
        tags.append(i)


element_counts = {}
for element in tags:
    count = tags.count(element)
    element_counts[element] = count 
    
print(element_counts)



sorted_counts = sorted(element_counts.items(), key=itemgetter(1), reverse=True)

sorted_counts = sorted_counts[:100]
for element, count in sorted_counts:
    print(element, count)
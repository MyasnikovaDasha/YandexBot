import json

d = {}
with open('russian_cities.json', encoding='utf-8') as file:
    data = json.load(file)
    for i in data:
        if i["city"][0] not in d.keys():
            d[i["city"][0]] = [i['city']]
        else:
            if i['city'] not in d[i["city"][0]]:
                d[i["city"][0]].append(i['city'])

with open("sorted_russian_cities.json", "w", encoding='utf-8') as file:
    json.dump(d, file, ensure_ascii=False, indent=2)
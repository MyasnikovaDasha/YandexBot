# Программа для сортировки словаря по алфавиту.
import json
with open('cities.json', encoding="utf-8") as city_file:
    city_data = json.load(city_file)
cities = []
for i in city_data["city"]:
    cities.append(i["name"])
result = {}
for i in cities:
    letter = i[0]
    if letter in result.keys():
        result[letter].append(i)
    else:
        result[letter] = [i]
with open("sorted_cities.json", mode="w", encoding="utf-8") as file:
    json.dump(result, file, ensure_ascii=False)
print(result)
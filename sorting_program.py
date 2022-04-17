from words import words
import json

d = {}
for i in range(len(words) - 1):
    if len(words[i]) == 1 and words[i] != '.':
        if ord(words[i]) < 1040 or ord(words[i]) > 1103:
            continue
    if words[i] not in d:
        d[words[i]] = []
    if words[i + 1] not in d[words[i]]:
        if len(words[i + 1]) == 1:
            if 1040 < ord(words[i + 1]) < 1103:
                pass
            else:
                continue
        d[words[i]].append(words[i + 1])

with open("sorted_words.json", "w", encoding='utf-8') as file:
    json.dump(d, file, ensure_ascii=False)
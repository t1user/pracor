import pprint
import json

with open('test_file') as file:
    data = json.loads(file.read())['included']

#pprint.pprint(data)

l = {}
try:
    for i in data:
        key = i['text']
        value = key.split(',')[0]
        l[key] = value
except:
    pass

pprint.pprint(l)

        
"""
    l.append(i['text'])

print(l)
"""

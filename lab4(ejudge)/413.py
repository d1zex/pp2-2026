import json
import re

data = json.loads(input())
q = int(input())
queries = [input() for _ in range(q)]

def resolve(obj, query):
    parts = re.findall(r'\w+|\[\d+\]', query)
    current = obj
    try:
        for part in parts:
            if part.startswith('['):
                index = int(part[1:-1])
                current = current[index]
            else:
                current = current[part]
        return json.dumps(current, separators=(',', ':'))
    except (KeyError, IndexError, TypeError):
        return "NOT_FOUND"

for query in queries:
    print(resolve(data, query))
import json

a = json.loads(input())
b = json.loads(input())

diffs = []

def format_value(v):
    if v == "<missing>":
        return "<missing>"
    return json.dumps(v, separators=(',', ':'))

def compare(d1, d2, path=""):
    keys = set(d1.keys()) | set(d2.keys())
    for key in sorted(keys):
        new_path = f"{path}.{key}" if path else key

        if key not in d1:
            v1 = "<missing>"
        else:
            v1 = d1[key]

        if key not in d2:
            v2 = "<missing>"
        else:
            v2 = d2[key]

        if isinstance(v1, dict) and isinstance(v2, dict):
            compare(v1, v2, new_path)
        elif v1 != v2:
            diffs.append(f"{new_path} : {format_value(v1)} -> {format_value(v2)}")

compare(a, b)

if diffs:
    for line in diffs:
        print(line)
else:
    print("No differences")
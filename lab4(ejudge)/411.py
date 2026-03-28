import json

source = json.loads(input())
patch = json.loads(input())

def apply_patch(src, p):
    for key, val in p.items():
        if val is None:
            if key in src:
                del src[key]
        elif isinstance(val, dict) and key in src and isinstance(src[key], dict):
            apply_patch(src[key], val)
        else:
            src[key] = val

apply_patch(source, patch)
print(json.dumps(source, sort_keys=True, separators=(',', ':')))

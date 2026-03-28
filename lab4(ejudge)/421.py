import importlib
import sys

input_lines = sys.stdin.read().splitlines()
q = int(input_lines[0])

for line in input_lines[1:]:
    module_path, attr_name = line.split()
    try:
        mod = importlib.import_module(module_path)
    except ModuleNotFoundError:
        print("MODULE_NOT_FOUND")
        continue
    if not hasattr(mod, attr_name):
        print("ATTRIBUTE_NOT_FOUND")
        continue
    if callable(getattr(mod, attr_name)):
        print("CALLABLE")
    else:
        print("VALUE")

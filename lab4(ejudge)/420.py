g = 0

def outer():
    n = 0
    def inner():
        nonlocal n
        global g
        num_cmds = int(input_lines.pop(0))  # first line is number of commands
        for _ in range(num_cmds):
            line = input_lines.pop(0).split()
            if len(line) != 2:
                continue  # skip invalid lines
            cmd, val = line
            val = int(val)
            if cmd == "global":
                g += val
            elif cmd == "nonlocal":
                n += val
            # ignore "local" or unknown commands
    inner()
    return n

import sys
input_lines = sys.stdin.read().splitlines()
n = outer()
print(g, n)
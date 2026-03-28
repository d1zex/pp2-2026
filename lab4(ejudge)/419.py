import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

d = math.hypot(x2 - x1, y2 - y1)

A = y2 - y1
B = x1 - x2
C = x2*y1 - x1*y2

dist_line = abs(C) / math.hypot(A, B)

dot1 = (x2-x1)*(-x1) + (y2-y1)*(-y1)
dot2 = (x1-x2)*(-x2) + (y1-y2)*(-y2)

if dist_line >= r or dot1 < 0 or dot2 < 0:
    print(f"{d:.10f}")
else:
    d1 = math.hypot(x1, y1)
    d2 = math.hypot(x2, y2)

    t1 = math.sqrt(d1*d1 - r*r)
    t2 = math.sqrt(d2*d2 - r*r)

    ang1 = math.atan2(y1, x1)
    ang2 = math.atan2(y2, x2)

    diff = abs(ang1 - ang2)
    diff = min(diff, 2*math.pi - diff)

    alpha = math.acos(r / d1)
    beta = math.acos(r / d2)

    arc = r * (diff - alpha - beta)

    result = t1 + t2 + arc

    print(f"{result:.10f}")
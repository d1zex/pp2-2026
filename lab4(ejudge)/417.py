import math

r = float(input())
x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

dx = x2 - x1
dy = y2 - y1
a = dx*dx + dy*dy
b = 2*(x1*dx + y1*dy)
c = x1*x1 + y1*y1 - r*r
discriminant = b*b - 4*a*c

if discriminant <= 0:
    # no intersection or tangent
    if x1*x1 + y1*y1 <= r*r and x2*x2 + y2*y2 <= r*r:
        length = math.hypot(dx, dy)
    else:
        length = 0.0
else:
    sqrt_d = math.sqrt(discriminant)
    t1 = (-b - sqrt_d)/(2*a)
    t2 = (-b + sqrt_d)/(2*a)
    t_low = max(0.0, min(t1, t2))
    t_high = min(1.0, max(t1, t2))
    if t_low > t_high:
        length = 0.0
    else:
        length = math.hypot(dx, dy)*(t_high - t_low)

print(f"{length:.10f}")

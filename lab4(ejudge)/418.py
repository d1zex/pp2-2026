x1, y1 = map(float, input().split())
x2, y2 = map(float, input().split())

# Mirror is x-axis (y=0)
# Reflect P2 over x-axis to get virtual point
xr = x2
yr = 0.0
# Using similar triangles: (xr - x1)/(0 - y1) = (x2 - xr)/(y2 - 0)
xr = (x2 * y1 + x1 * y2) / (y1 + y2)
print(f"{xr:.10f} 0.0000000000")

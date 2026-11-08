"""Independent scalar check: an affine field is reproduced by a centered quadratic B-spline.

For |t|<=1/2, B2(t)=3/4-t*t. For 1/2<|t|<3/2,
B2(t)=(3/2-|t|)**2/2. At integer interior coordinates its weights
are 1/8, 3/4, 1/8, which preserve 10+x+2*y exactly.
All 25 grid coordinates lie in their own library's support.
"""
import json

def spline(t):
    t = abs(t)
    return .75-t*t if t <= .5 else ((1.5-t)**2/2 if t < 1.5 else 0)

values = []
for y in (-1, 0, 1):
    row = []
    for x in (-1, 0, 1):
        row.append(sum((10+i+2*j)*spline(x-i)*spline(y-j)
                       for j in range(-2, 3) for i in range(-2, 3)))
    values.append(row)
assert values == [[7., 8., 9.], [9., 10., 11.], [11., 12., 13.]]
print(json.dumps({'yield': values, 'masked_library_grid_pixels': 0,
                  'normal': [[1.]*3 for _ in range(3)]}, indent=2))

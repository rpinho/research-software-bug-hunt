"""Independent bookkeeping: save/load preserves masks; adding one mask unions the sets."""
import json
rows = [[1000., 2., 3.], [4., 5., 6.], [7., 8., 9.]]
old = {(0, 0)}
new = old | {(2, 2)}
mask = lambda cells: [[(r, c) in cells for c in range(3)] for r in range(3)]
count = lambda cells: sum(rows[r][c] for r in range(3) for c in range(3) if (r, c) not in cells)
print(json.dumps({'loaded_pixels_mask': mask(old), 'edited_mask': mask(new),
                  'edited_sum': count(new), 'saved_again_sum': count(new),
                  'normal': {'sum': count({(2, 2)}), 'mask': mask({(2, 2)})}}, indent=2))

import numpy as np
from pyfdd import DataPattern
from common import finish, matrix, work

folder = work()
data = np.array([[1000., 2., 3.], [4., 5., 6.], [7., 8., 9.]])
p = DataPattern(pattern_array=data)
p.mask_pixel(0, 0)
p.io_save_json(str(folder / 'saved.json'))
q = DataPattern(str(folder / 'saved.json'))
loaded_pixels = q.pixels_mask.tolist()
q.mask_pixel(2, 2)
q.io_save_json(str(folder / 'saved-again.json'))
r = DataPattern(str(folder / 'saved-again.json'))
# A normal file without masks still has the same values after load/edit.
n = DataPattern(pattern_array=data)
n.io_save_json(str(folder / 'normal.json'))
n = DataPattern(str(folder / 'normal.json'))
n.mask_pixel(2, 2)
finish({'loaded_pixels_mask': loaded_pixels, 'edited_mask': q.pattern_matrix.mask.tolist(),
        'edited_sum': float(q.pattern_matrix.sum()), 'saved_again_sum': float(r.pattern_matrix.sum()),
        'normal': {'sum': float(n.pattern_matrix.sum()), 'mask': n.pattern_matrix.mask.tolist()}})

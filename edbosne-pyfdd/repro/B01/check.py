import numpy as np
from pyfdd import Lib2dl, PatternCreator
from common import finish, library_path, matrix, work

lib = Lib2dl(library_path(work()))
x, y = np.meshgrid([-1., 0., 1.], [-1., 0., 1.])
g = PatternCreator(lib, x, y, simulations=(1,))
yield_values = g.make_pattern(0, 0, 0, [1], 1, pattern_type='yield')
flat = g.make_pattern(0, 0, 0, [0], 1, pattern_type='yield')
grid = PatternCreator(lib, simulations=(1,))
edge = grid.make_pattern(0, 0, 0, [0], 1, pattern_type='yield')
finish({'yield': matrix(yield_values), 'masked_library_grid_pixels': int(np.ma.getmaskarray(edge).sum()),
        'normal': matrix(flat)})

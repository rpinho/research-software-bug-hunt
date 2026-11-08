import numpy as np
from pyfdd import DataPattern
from common import finish

cases = {}
for command in ('cw', 'cc', 'mh', 'mv', 'cw,mh'):
    p = DataPattern(pattern_array=np.array([[1000., 2., 3.], [4., 5., 6.], [7., 8., 9.]]))
    p.mask_pixel(0, 0)
    p.set_fit_region(-.25, center=(1, 1))  # masks the central pixel separately
    p.manip_orient(command)
    p.mask_pixel(2, 2)
    cases[command] = {'mask': p.pattern_matrix.mask.tolist(), 'sum': float(p.pattern_matrix.sum())}
p = DataPattern(pattern_array=np.array([[1000., 2., 3.], [4., 5., 6.]]))
p.mask_pixel(0, 0)
p.manip_orient('cw')
try:
    p.mask_pixel(2, 1)
    rectangular = {'mask': p.pattern_matrix.mask.tolist(), 'sum': float(p.pattern_matrix.sum())}
except Exception as e:
    rectangular = {'error': type(e).__name__}
n = DataPattern(pattern_array=np.ones((3, 3)))
n.manip_orient('cw')
n.mask_pixel(2, 2)
finish({'commands': cases, 'rectangular': rectangular,
        'normal': {'sum': float(n.pattern_matrix.sum()), 'mask': n.pattern_matrix.mask.tolist()}})

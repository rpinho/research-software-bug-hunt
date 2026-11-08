import numpy as np
from pyfdd import Lib2dl, Fit
from common import finish, library_path, work

lib = Lib2dl(library_path(work()))
x, y = np.meshgrid([-1.,0.,1.],[-1.,0.,1.])
f = Fit(lib,(1,))  # six active parameters: dx,dy,phi,total_cts,sigma,f_p1
f.set_data_pattern(x,y,np.ma.array(np.ones((3,3))))  # NumPy's default scalar nomask
scalar_dof = int(f.get_dof())
f.set_data_pattern(x,y,np.ones((3,3)))
try:
    array_dof = int(f.get_dof())
except Exception as e:
    array_dof = {'error': type(e).__name__, 'message': str(e)}
mask = np.zeros((3,3),dtype=bool)
mask[0,0] = True
f.set_data_pattern(x,y,np.ma.array(np.ones((3,3)),mask=mask))
finish({'scalar_nomask_dof': scalar_dof, 'ndarray_dof': array_dof,
        'normal': {'explicit_mask_dof': int(f.get_dof())}})

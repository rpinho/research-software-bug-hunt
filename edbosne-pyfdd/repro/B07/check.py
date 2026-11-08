import numpy as np
from pyfdd import Lib2dl, Fit
from common import library_path, work, finish

lib=Lib2dl(library_path(work()))
x,y=np.meshgrid([-1.,0.,1.],[-1.,0.,1.])

def fitting(scale):
    f=Fit(lib,(1,))
    f.set_data_pattern(x,y,np.ma.array(np.ones((3,3))*10.,mask=False))
    f.set_initial_values(dx=0,dy=0,phi=0,total_cts=90.,sigma=0,f_p1=0)
    f.fix_parameters(dx=True,dy=True,phi=True,total_cts=False,sigma=True,f_p1=True)
    f.set_scale_values(total_cts=scale)
    f.minimize_chi2()
    return f

errors={}
for scale in (1.,10.):
    f=fitting(scale)
    std=f.get_std_from_hessian(f.results.x,func='chi2')[0]
    errors[str(int(scale))]={'fitted_total':float(f.results.x[0]),'std':float(format(float(std), '.7g'))}
# A nonzero chi-square value is unchanged by the zero-minimum guard.
n=fitting(1.)
n.previous_cost_value=None
normal=float(n.chi_square_call([80.],enable_scale=True))
finish({'parameter_scales':errors,'normal':{'chi2_at_80_counts':normal}})

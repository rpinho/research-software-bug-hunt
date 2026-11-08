import math
import struct
import numpy as np
from pyfdd import Lib2dl, Fit, PatternCreator
from common import record, work, finish

folder=work()
p=np.ones((7,7)); p[2:5,2:5]=0
header=struct.pack('<hh8f',7,7,0,0,1,1,-3,-3,0,0)
site=struct.pack('<h50s3f',1,b'nonnegative zero plateau',1,0,0)
path=folder/'zero.2dl'
path.write_bytes(b'K'+record(header)+record(site)+record(struct.pack('<49f',*p.ravel()))+bytes([130]))
lib=Lib2dl(str(path))
x,y=np.meshgrid([-1.,0.,1.],[-1.,0.,1.])
f=Fit(lib,(1,))

def evaluate(counts, fraction, mask=False):
    f.set_data_pattern(x,y,np.ma.array(counts,mask=mask))
    f.pattern_generator=PatternCreator(lib,x,y,(1,),mask=f.data_pattern.mask,mask_out_of_range=False)
    ll=float(f.log_likelihood(0,0,0,[fraction]))
    chi=float(f.chi_square(0,0,0,9,[fraction]))
    show=lambda v: 'infinity' if math.isinf(v) and v>0 else v
    return {'nll': show(ll), 'chi2': show(chi)}

impossible=evaluate(np.ones((3,3)),1)
zero_counts=np.ones((3,3)); zero_counts[1,1]=0
empty=evaluate(zero_counts,1)
normal=evaluate(np.ones((3,3)),0)
finish({'positive_count_zero_probability': impossible, 'zero_count_zero_probability': empty, 'normal': normal})

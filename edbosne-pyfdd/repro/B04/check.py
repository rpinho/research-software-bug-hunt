import numpy as np
from pyfdd import Lib2dl, PatternCreator
from common import finish, library_path, matrix, work

lib = Lib2dl(library_path(work()))
x, y = np.meshgrid([-1.,0.,1.], [-1.,0.,1.])
background = np.ones((3,3))
g = PatternCreator(lib,x,y,simulations=(1,),background_pattern=background,background_factor=2)
first = g.make_pattern(0,0,0,[0],90)
# Move into the edge of the library, then return to the original parameters.
g.make_pattern(2,0,0,[0],90)
again = g.make_pattern(0,0,0,[0],90)
# Repeat an ordinary in-range call on a fresh instance.
n = PatternCreator(lib,x,y,simulations=(1,),background_pattern=np.ones((3,3)),background_factor=2)
n.make_pattern(0,0,0,[0],90)
normal = n.make_pattern(0,0,0,[0],90)
finish({'first': matrix(first), 'after_excursion': matrix(again),
        'masked_after_excursion': int(np.ma.getmaskarray(again).sum()),
        'normal': matrix(normal)})

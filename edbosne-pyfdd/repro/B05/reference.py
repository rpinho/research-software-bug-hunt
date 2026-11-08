"""Independent definition: number of observed bins minus number of fitted parameters."""
import json
parameters = ('dx','dy','phi','total_cts','sigma','f_p1')
unmasked_bins = [(r,c) for r in range(3) for c in range(3)]
print(json.dumps({'scalar_nomask_dof': len(unmasked_bins)-len(parameters),
                  'ndarray_dof': len(unmasked_bins)-len(parameters),
                  'normal': {'explicit_mask_dof': len(unmasked_bins)-1-len(parameters)}}, indent=2))

"""Independent mixture: uniform signal plus uniform background stays uniform.

At the initial and final identical mesh, all nine pixels are in range.
Each has probability (1/2)*(1/9)+(1/2)*(1/9)=1/9, hence 10 counts.
A previous request with another displacement is absent from this definition.
"""
import json
uniform = [[90*(.5/9+.5/9) for _ in range(3)] for _ in range(3)]
print(json.dumps({'first': uniform, 'after_excursion': uniform,
                  'masked_after_excursion': 0, 'normal': uniform}, indent=2))

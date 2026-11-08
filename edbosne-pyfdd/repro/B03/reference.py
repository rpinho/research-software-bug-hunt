"""Independent index mapping, no NumPy rotations: move each value and each mask together."""
import json

def orient(rows, excluded, commands):
    for cmd in commands.split(','):
        nr, nc = len(rows), len(rows[0])
        mapping = {'cw': lambda r,c: (c,nr-1-r), 'cc': lambda r,c: (nc-1-c,r),
                   'mh': lambda r,c: (r,nc-1-c), 'mv': lambda r,c: (nr-1-r,c)}[cmd]
        height, width = (nc,nr) if cmd in ('cw','cc') else (nr,nc)
        out = [[0.]*width for _ in range(height)]
        for r in range(nr):
            for c in range(nc):
                rr, cc = mapping(r,c)
                out[rr][cc] = rows[r][c]
        rows, excluded = out, {mapping(r,c) for r,c in excluded}
    return rows, excluded

def answer(rows, excluded, commands, added):
    rows, excluded = orient(rows, excluded, commands)
    excluded |= {added}
    return {'mask': [[(r,c) in excluded for c in range(len(row))] for r,row in enumerate(rows)],
            'sum': sum(v for r,row in enumerate(rows) for c,v in enumerate(row) if (r,c) not in excluded)}

rows = [[1000.,2.,3.],[4.,5.,6.],[7.,8.,9.]]
commands = {cmd: answer(rows,{(0,0),(1,1)},cmd,(2,2)) for cmd in ('cw','cc','mh','mv','cw,mh')}
print(json.dumps({'commands': commands, 'rectangular': answer(rows[:2],{(0,0)},'cw',(2,1)),
                  'normal': answer([[1.]*3 for _ in range(3)],set(),'cw',(2,2))}, indent=2))

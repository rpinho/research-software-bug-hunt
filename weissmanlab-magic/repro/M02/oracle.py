"""The README's gamma-mixture row format and direct exponential mixture transform."""
def reference():
 return {'gamma_row':[0.5,1.,1.], 'zero_row':[0.5],
         'laplace_points':[[s,0.5+0.5/(1+s)] for s in [1.,2.,4.]],
         'zero_mass_format':'one row containing a single column'}

def read_distribution(text):
 rows=[[float(x) for x in line.split()] for line in text.splitlines() if line.strip()]
 assert len(rows[-1])==1
 assert all(len(r)==3 for r in rows[:-1])
 assert abs(sum(r[0] for r in rows)-1)<1e-10
 return rows

def transform(rows,s):
 return sum(r[0] if len(r)==1 else r[0]*(1+r[2]*s)**(-r[1]) for r in rows)

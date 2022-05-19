import math
import sympy

n = 1216177716507739302616478655910148392804849
p = 1033247481589406269253
q = 1177043968824330681533
e = 65537

c1 = 257733734393970582988408159581244878149116
c2 = 843105902970788695411197846605744081831851
assert n == p * q

phi = (p - 1) * (q - 1)

d = sympy.mod_inverse(e, phi)

m = pow(c1, d, n)
print(m.to_bytes(14, 'big'))
m = pow(c2, d, n)
print(m.to_bytes(14, 'big'))
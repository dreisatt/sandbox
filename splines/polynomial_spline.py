from sympy import *
import numpy as np
import scipy.linalg as l
import pylab as p

import re

def replace_pow(m):
    return 'std::pow(t,' + m.group(1) + ')'

t = symbols('t')
y = symbols('y')
g = symbols('g')

def gen_polynomial(degree):
	T = []
	C = []
	for i in range(degree):
		T.append(t**i)
		C.append(symbols('c'+str(i)))
	return Matrix(T), Matrix(C)

def gen_polynomial_yaw(degree):
	Y = []
	U = []
	for i in range(degree):
		Y.append(y**i)
		U.append(symbols('u'+str(i)))
	return Matrix(Y), Matrix(U)

def print_matrix_line(pol, t_val):
	for v in pol.subs({t:t_val}).jacobian(C):
		print(str(v) + ',')
	print

T,C = gen_polynomial(12)
Y,U = gen_polynomial_yaw(8)

pol_yaw = U.T*Y
pol_yaw_d1 = pol_yaw.diff(y)
pol_yaw_d2 = pol_yaw.diff(y, y)

p0y = pol_yaw.jacobian(U)
p1y = pol_yaw_d1.jacobian(U)
p2y = pol_yaw_d2.jacobian(U)

pol = C.T*T
pol_d1 = pol.diff(t)
pol_d2 = pol.diff(t, t)
pol_d3 = pol.diff(t, t, t)
pol_d4 = pol.diff(t, t, t, t)

p0 = pol.jacobian(C)
p1 = pol_d1.jacobian(C)
p2 = pol_d2.jacobian(C)
p3 = pol_d3.jacobian(C)
p4 = pol_d4.jacobian(C)

'''
print_matrix_line(pol, 0)
print_matrix_line(pol, 1)

print_matrix_line(pol_d1, 0)
print_matrix_line(pol_d1, 1)

print_matrix_line(pol_d2, 0)
print_matrix_line(pol_d2, 1)

print_matrix_line(pol_d3, 0)
print_matrix_line(pol_d3, 1)

print_matrix_line(pol_d4, 0)
print_matrix_line(pol_d4, 1)
'''

# Computing Hessian of pol_d2**2

J = (pol_d3**2).jacobian(C)
H = J.jacobian(C)
H_int = integrate(H, t)

J_yaw = (pol_yaw_d1**2).jacobian(U)
H_yaw = J_yaw.jacobian(U)
H_yaw_int = integrate(H_yaw, y)

J1 = pol_d2.jacobian(C)
J1_int = integrate(J1, t)

F_yaw = U.T*H_yaw*U/2
F_yaw.simplify()
F = C.T*H*C/2 + 2*g*J1 * C + Matrix([g])**2
F.simplify()

F1 = (pol_d2 + Matrix([g])) **2

polynome = poly(F[0])
polynome1 = poly(F1[0])

if polynome == polynome1:
    print('polynome == polynome1')
else:
    print('polynome != polynome1')

points = [1.0, 9.0, 8.0, 3.0, 5.0, 3.0]
time = [0.0, 0.2, 0.4, 0.6, 0.8, 2]

#points = [1 ,10]
#time = [0.0, 2.0]


n = len(time)



'''
print 'typedef Eigen::Matrix<double, 12, 12> Matrix12;\n'
print 'typedef Eigen::Matrix<double, 12, 1> Vector12;\n'
print 'void compute_Q(Matrix12 & Q, double t) {'

for i in range(12):
    for j in range(12):
        print '    Q(' + str(i) + ',' + str(j) + ') = ' + re.sub(r't\*\*([0-9]+)', replace_pow, str(H_int[i,j])) + ';'

print '}\n\n'

print 'void compute_pol(Vector12 & pol, double t, int deriv=0) {'
print '    if (deriv == 0) {'
for i in range(12):
    print '        pol(' + str(i) + ') = ' + re.sub(r't\*\*([0-9]+)', replace_pow, str(p0[i])) + ';'
print '    }'

print '    if (deriv == 1) {'
for i in range(12):
    print '        pol(' + str(i) + ') = ' + re.sub(r't\*\*([0-9]+)', replace_pow, str(p1[i])) + ';'
print '    }'

print '    if (deriv == 2) {'
for i in range(12):
    print '        pol(' + str(i) + ') = ' + re.sub(r't\*\*([0-9]+)', replace_pow, str(p2[i])) + ';'
print '    }'

print '    if (deriv == 3) {'
for i in range(12):
    print '        pol(' + str(i) + ') = ' + re.sub(r't\*\*([0-9]+)', replace_pow, str(p3[i])) + ';'
print '    }'

print '    if (deriv == 4) {'
for i in range(12):
    print '        pol(' + str(i) + ') = ' + re.sub(r't\*\*([0-9]+)', replace_pow, str(p4[i])) + ';'
print '    }'
print '}'

'''

# Quadratic cost (http://en.wikipedia.org/wiki/Quadratic_programming)
Q = np.zeros((12*(n-1), 12*(n-1)))
c = np.zeros(12*(n-1))

# Constraints matrix
E = np.zeros((10 + 6*(n-2), 12*(n-1)))
d = np.zeros(10 + 6*(n-2))

for i in range(n-1):
    Q[12*i:12*(i+1), 12*i:12*(i+1)] = np.array(H_int.evalf(subs={t:time[i+1]})).astype(np.float64) - np.array(H_int.evalf(subs={t:time[i]})).astype(np.float64)
    c[12*i:12*(i+1)] = -2*9.8* (np.array(J1_int.evalf(subs={t:time[i+1]})).astype(np.float64) - np.array(J1_int.evalf(subs={t:time[i]})).astype(np.float64))


E[0, :12] = np.array(pol.jacobian(C).evalf(subs={t:time[0]})).astype(np.float64)
E[1, :12] = np.array(pol_d1.jacobian(C).evalf(subs={t:time[0]})).astype(np.float64)
E[2, :12] = np.array(pol_d2.jacobian(C).evalf(subs={t:time[0]})).astype(np.float64)
E[3, :12] = np.array(pol_d3.jacobian(C).evalf(subs={t:time[0]})).astype(np.float64)
E[4, :12] = np.array(pol_d4.jacobian(C).evalf(subs={t:time[0]})).astype(np.float64)
d[0] = points[0]
d[1] = 0
d[2] = 0
d[3] = 0
d[4] = 0


E[5, 12*(n-2):] = np.array(pol.jacobian(C).evalf(subs={t:time[-1]})).astype(np.float64)
E[6, 12*(n-2):] = np.array(pol_d1.jacobian(C).evalf(subs={t:time[-1]})).astype(np.float64)
E[7, 12*(n-2):] = np.array(pol_d2.jacobian(C).evalf(subs={t:time[-1]})).astype(np.float64)
E[8, 12*(n-2):] = np.array(pol_d3.jacobian(C).evalf(subs={t:time[-1]})).astype(np.float64)
E[9, 12*(n-2):] = np.array(pol_d4.jacobian(C).evalf(subs={t:time[-1]})).astype(np.float64)
d[5] = points[-1]
d[6] = 0
d[7] = 0
d[8] = 0
d[9] = 0


for i in range(n-2):
    E[10+6*i+0, 12*(i+0):12*(i+1)] = np.array(pol.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)
    E[10+6*i+1, 12*(i+1):12*(i+2)] = np.array(pol.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)

    E[10+6*i+2, 12*(i+0):12*(i+1)] = np.array(pol_d1.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)
    E[10+6*i+2, 12*(i+1):12*(i+2)] = -np.array(pol_d1.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)

    E[10+6*i+3, 12*(i+0):12*(i+1)] = np.array(pol_d2.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)
    E[10+6*i+3, 12*(i+1):12*(i+2)] = -np.array(pol_d2.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)

    E[10+6*i+4, 12*(i+0):12*(i+1)] = np.array(pol_d3.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)
    E[10+6*i+4, 12*(i+1):12*(i+2)] = -np.array(pol_d3.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)

    E[10+6*i+5, 12*(i+0):12*(i+1)] = np.array(pol_d4.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)
    E[10+6*i+5, 12*(i+1):12*(i+2)] = -np.array(pol_d4.jacobian(C).evalf(subs={t:time[i+1]})).astype(np.float64)
    
    d[10+6*i+0] = points[i+1]
    d[10+6*i+1] = points[i+1]
    d[10+6*i+2] = 0
    d[10+6*i+3] = 0
    d[10+6*i+4] = 0
    d[10+6*i+5] = 0
    


A = np.zeros((12*(n-1)+10+6*(n-2), 12*(n-1)+10+6*(n-2)))
b = np.zeros(12*(n-1)+10+6*(n-2))

A[0:12*(n-1), 0:12*(n-1)] = Q
A[0:12*(n-1), 12*(n-1):] = E.T
A[12*(n-1):, 0:12*(n-1)] = E

b[:12*(n-1)] = c
b[12*(n-1):] = d

np.savetxt('A_py.txt', A, fmt='%.20f')
np.savetxt('b_py.txt', b)


#print 'A.shape', A.shape
#for i in range(A.shape[0]):
#    for j in range (A.shape[1]):
#        print '%8f ' % A[i,j],
#    print ' '

#print 'A', A
#print 'b.shape', b.shape
#print 'b', b

lu_res = l.lu_factor(A)
res = l.lu_solve(lu_res, b)

np.savetxt('res_py.txt', res)

coeffs = res[0:12*(n-1)]

print('coeffs', coeffs)

#coeffs = np.loadtxt('coeffs_cpp.txt')
#print 'coeffs', coeffs

t = np.arange(0,2,0.001)
T = np.vstack([t**0, t**1, t**2, t**3, t**4, t**5, t**6, t**7, t**8, t**9, t**10, t**11]).transpose()


res = np.zeros_like(t)
res_d2 = np.zeros_like(t)
J_d2 = np.array([0, 0, 2, 6, 12, 20, 30, 42, 56, 72, 90, 110])

for i in range(n-1):
    idx = np.logical_and(t >= time[i], t <= time[i+1])
    res[idx] = np.dot(T[idx], coeffs[12*i:12*(i+1)])
    coeffs_d2 = J_d2 * coeffs[12*i:12*(i+1)]
    print('coeffs', coeffs)
    print('coeffs_d2', coeffs_d2)
    res_d2[idx] = np.dot(T[idx], coeffs_d2)
    
work = np.sum((res_d2 + 9.8)**2)
print('work', work)



p.plot(t, res, 'b')
p.plot(t, res_d2, 'g')
p.plot(time, points, 'ro')
p.show()


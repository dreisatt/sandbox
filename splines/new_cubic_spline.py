import numpy as np
from multipledispatch import dispatch
import matplotlib.pyplot as plt

class CubicPolynomial:
    def __init__(self, c0=0.0, c1=0.0, c2=0.0, c3=0.0, shift=0.0):
        self.c0 = c0
        self.c1 = c1
        self.c2 = c2
        self.c3 = c3
        self.shift = shift

    @dispatch(float)
    def evaluate(self, t):
        delta = t-self.shift
        return self.c0 + delta*(self.c1 + delta*(self.c2 + self.c3*delta))

    @dispatch(np.ndarray)
    def evaluate(self, times):
        return [self.evaluate(t) for t in times]

    def evaluateFirstDerivative(self, t):
        delta = t-self.shift
        return self.c1 + delta*(2.0*self.c2 + 3.0*self.c3*delta)

    def evaluateSecondDerivative(self, t):
        return 2.0*self.c2 + 6.0*self.c3*(t-self.shift)

def segmentTimes(waypoints, total_time):
    dist = []
    for i in range(waypoints.shape[0]-1):
        dist.append(np.linalg.norm(waypoints[i]-waypoints[i+1]))
    total_dist = sum(dist)
    return [item*total_time/total_dist for item in dist]

class CubicSpline:
    def __init__(self, durations=[], control_points=None):
        self.durations = durations
        self.segments = len(durations)-1
        self.polynomials = []
        if control_points == None:
            self.control_points = []
        else:
            self.control_points = control_points
            self._computeSplineCoefficient()
        self.segment = 0

    def addControlPoints(self, control_points):
        self.control_points = control_points
        self._computeSplineCoefficient()

    def evaluate(self, t):
        if t <= duration[self.segment+1]:
            return self.polynomials[self.segment-1].evaluate(t)
        else:
            # TODO::Niko: Implement binary search
            CubicSpline.i = CubicSpline.i + 1
            return self.polynomials[CubicSpline.i-1].evaluate(t)

    def _computeSplineCoefficient(self):
        A = np.zeros((4*self.segments, 4*self.segments))
        b = np.zeros((4*self.segments, 1))

        A[2][1] = 1.0
        A[3][(self.segments-1)*4+1] = 1.0
        delta = self.durations[-1]-self.durations[-2]
        A[3][(self.segments-1)*4+2] = 2.0*delta
        A[3][(self.segments-1)*4+3] = 3.0*delta*delta
        for i in range(self.segments):
            A[4*i][4*i] = 1.0
            b[4*i] = self.control_points[i]

            A[4*i+1][4*i] = 1.0
            delta = self.durations[i+1]-self.durations[i]
            A[4*i+1][4*i+1] = delta
            A[4*i+1][4*i+2] = delta*delta
            A[4*i+1][4*i+3] = A[4*i+1][4*i+2] * delta
            b[4*i+1] = self.control_points[i+1]

            if i == 0:
                continue

            A[i*4+2][(i-1)*4] = 0.0
            A[i*4+2][(i-1)*4+1] = 1.0
            delta = self.durations[i]-self.durations[i-1]
            A[i*4+2][(i-1)*4+2] = 2.0*delta
            A[i*4+2][(i-1)*4+3] = 3.0*delta*delta
            # First derivative condition (right hand side)
            A[i*4+2][i*4+1] = -1.0
            # Second derivative condition (left hand side)
            A[i*4+3][(i-1)*4+2] = 2.0
            A[i*4+3][(i-1)*4+3] = 6.0*delta
            # Second derivative condition (right hand side)
            A[i*4+3][i*4+2] = -2.0
        x = np.linalg.solve(A, b)
        x = x.reshape(self.segments, 4)
        for i in range(segments):
            self.polynomials.append(CubicPolynomial(x[i][0], x[i][1], x[i][2], x[i][3], self.duration[i]))

class CubicSpline2D:
    def __init__(self, t_start, t_end):
        self.durations = self._computeSegmentDuration(t_start, t_end)
        self.control_points = None
        self.xSpline = CubicSpline(self.durations)
        self.ySpline = CubicSpline(self.durations)

    def addControlPoints(self, control_points):
        x = []
        y = []
        for point in control_points:
            x.append(point[0])
            y.append(point[0])
        self.xSpline.addControlPoints(x)
        self.ySpline.addControlPoints(y)

    def _computeSegmentDuration(self, t_start, t_end):
        total_time = t_end-t_start
        dist = []
        for i in range(self.control_points.shape[0]-1):
            dist.append(np.linalg.norm(self.control_points[i]-self.control_points[i+1]))
        total_dist = sum(dist)
        segment_durations = [item*total_time/total_dist for item in dist]
        durations = [t_start]
        for segment_duration in segment_durations:
            durations.append(duration[-1] + segment_duration)
        return durations

    def evaluate(self, t):
        x = self.xSpline.evaluate(t)
        y = self.ySpline.evaluate(t)
        return x,y

t_start = 0.0
t_end = 1.0
x_input = [3.0, 5.0, 2.0, 6.0, 8.0, 10.0]
y_input = [1.0, 4.0, 6.25, 0.0, 2.0, -5.0]
waypoints = np.empty((len(x_input), 2))
for i in range(len(x_input)):
    waypoints[i][0] = x_input[i]
    waypoints[i][1] = y_input[i]
segments = len(x_input)-1
segment_durations = segmentTimes(waypoints, t_end-t_start)
duration = [t_start]
for segment_time in segment_durations:
    duration.append(duration[-1] + segment_time)

A = np.zeros((4*segments, 4*segments))
bx = np.zeros((4*segments, 1))
by = np.zeros((4*segments, 1))
A[2][1] = 1.0
A[3][(segments-1)*4+1] = 1.0
delta = duration[-1]-duration[-2]
A[3][(segments-1)*4+2] = 2.0*delta
A[3][(segments-1)*4+3] = 3.0*delta*delta
for i in range(segments):
    A[4*i][4*i] = 1.0
    bx[4*i] = x_input[i]
    by[4*i] = y_input[i]

    A[4*i+1][4*i] = 1.0
    delta = duration[i+1]-duration[i]
    A[4*i+1][4*i+1] = delta
    A[4*i+1][4*i+2] = delta*delta
    A[4*i+1][4*i+3] = A[4*i+1][4*i+2] * delta
    bx[4*i+1] = x_input[i+1]
    by[4*i+1] = y_input[i+1]

    if i == 0:
        continue

    A[i*4+2][(i-1)*4] = 0.0
    A[i*4+2][(i-1)*4+1] = 1.0
    delta = duration[i]-duration[i-1]
    A[i*4+2][(i-1)*4+2] = 2.0*delta
    A[i*4+2][(i-1)*4+3] = 3.0*delta*delta
    # First derivative condition (right hand side)
    A[i*4+2][i*4+1] = -1.0
    # Second derivative condition (left hand side)
    A[i*4+3][(i-1)*4+2] = 2.0
    A[i*4+3][(i-1)*4+3] = 6.0*delta
    # Second derivative condition (right hand side)
    A[i*4+3][i*4+2] = -2.0

print(A)
x = np.linalg.solve(A, bx)
y = np.linalg.solve(A, by)
x = x.reshape(segments, 4)
y = y.reshape(segments, 4)
t1 = np.linspace(t_start, duration[1], 70)
t2 = np.linspace(duration[1], duration[2], 70)
t3 = np.linspace(duration[2], t_end, 70)
t_test = np.concatenate([t1, t2, t3])

x_polynomials = []
y_polynomials = []
for i in range(segments):
    x_polynomials.append(CubicPolynomial(x[i][0], x[i][1], x[i][2], x[i][3], duration[i]))
    y_polynomials.append(CubicPolynomial(y[i][0], y[i][1], y[i][2], y[i][3], duration[i]))
x_spline = []
y_spline = []
t = None
for i in range(segments):
    t_seg = np.linspace(duration[i], duration[i+1], 100)
    x_values = x_polynomials[i].evaluate(t_seg)
    y_values = y_polynomials[i].evaluate(t_seg)
    x_spline.extend(x_values)
    y_spline.extend(y_values)
    if t is None:
        t = t_seg
    else:
        t = np.concatenate([t, t_seg])
first_polynomial = CubicPolynomial(x[0][0], x[0][1], x[0][2], x[0][3])
second_polynomial = CubicPolynomial(x[1][0], x[1][1], x[1][2], x[1][3], duration[1])
third_polynomial = CubicPolynomial(x[2][0], x[2][1], x[2][2], x[2][3], duration[2])
spline_test = []
first_polynom = []
second_polynom = []
third_polynom = []

for step in t1:
    first_polynom.append(first_polynomial.evaluate(step))

for step in t2:
    second_polynom.append(second_polynomial.evaluate(step))

for step in t:
    third_polynom.append(third_polynomial.evaluate(step))

for step in t1:
    spline_test.append(first_polynomial.evaluate(step))

for step in t2:
    spline_test.append(second_polynomial.evaluate(step))

for step in t3:
    spline_test.append(third_polynomial.evaluate(step))

print(duration)
print(first_polynomial.evaluate(duration[1]))
print(second_polynomial.evaluateFirstDerivative(duration[1]))

print(second_polynomial.evaluate(duration[2]))
print(third_polynomial.evaluate(duration[2]))

plt.figure()
plt.plot(t, x_spline)
plt.plot(t, y_spline)
plt.plot(duration, x_input, 'x')
plt.plot(duration, y_input, 'o')
plt.show(block=False)

plt.figure()
plt.plot(x_spline, y_spline)
plt.plot(x_input, y_input, 'x')
plt.show(block=False)

plt.show()
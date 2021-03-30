import numpy as np
import math
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
        # TODO::Niko: Rename to segment_number
        self.segments = len(durations)-1
        self.polynomials = []
        if control_points == None:
            self.control_points = []
        else:
            self.control_points = control_points
            self._computeSplineCoefficient()
        self.segment = 0

    def getSegments(self):
        return self.segments

    def addControlPoints(self, control_points):
        self.control_points = control_points
        self._computeSplineCoefficient()

    @dispatch(float)
    def evaluate(self, t):
        # TODO::Niko: Implement binary search or something mapping from t to segment
        if t > duration[self.segment+1]:
            self.segment = self.segment + 1
        return self.polynomials[self.segment].evaluate(t)

    @dispatch(int)
    def evaluate(self, segment):
        if segment <= self.segments:
            times = np.linspace(self.durations[segment], self.durations[segment+1], 100)
            return times, self.polynomials[segment].evaluate(times)
        else:
            raise ValueError("Invalid segment id: ", segment)

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
            self.polynomials.append(CubicPolynomial(x[i][0], x[i][1], x[i][2], x[i][3], self.durations[i]))

class CubicSpline2D:
    def __init__(self, t_start, t_end):
        self.control_points = []
        self.t_start = t_start
        self.t_end = t_end

    def addControlPoints(self, control_points):
        self.control_points = control_points
        durations = self._computeSegmentDuration(self.t_start, self.t_end)
        x = []
        y = []
        for point in control_points:
            x.append(point[0])
            y.append(point[1])
        self.xSpline = CubicSpline(durations)
        self.ySpline = CubicSpline(durations)
        self.xSpline.addControlPoints(x)
        self.ySpline.addControlPoints(y)

    def _computeSegmentDuration(self, t_start, t_end):
        total_time = t_end-t_start
        dist = []
        for i in range(len(self.control_points)-1):
            dist.append(self._computeNorm(self.control_points[i], self.control_points[i+1]))
        total_dist = sum(dist)
        segment_durations = [item*total_time/total_dist for item in dist]
        durations = [t_start]
        for segment_duration in segment_durations:
            durations.append(durations[-1] + segment_duration)
        return durations

    def _computeNorm(self, first, second):
        x_dist = first[0] - second[0]
        y_dist = first[1] - second[1]
        return math.sqrt(x_dist*x_dist + y_dist*y_dist)

    def evaluate(self, segment):
        tx, x = self.xSpline.evaluate(segment)
        ty, y = self.ySpline.evaluate(segment)
        return x, y

    def getNumberOfSegments(self):
        return self.xSpline.getSegments()

if __name__=='__main__':
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

    x_spline = CubicSpline(duration)
    y_spline = CubicSpline(duration)
    x_spline.addControlPoints(x_input)
    y_spline.addControlPoints(y_input)
    x_values = []
    y_values = []
    t = None
    for i in range(x_spline.getSegments()):
        tsx, x_segment = x_spline.evaluate(i)
        tsy, y_segment = y_spline.evaluate(i)
        x_values.extend(x_segment)
        y_values.extend(y_segment)
        if t is None:
            t = tsx
        else:
            t = np.concatenate([t, tsx])
    plt.figure()
    plt.plot(t, x_values)
    plt.plot(t, y_values)
    plt.plot(duration, y_input, 'x')
    plt.plot(duration, x_input, 'o')
    plt.show(block=False)

    spline = CubicSpline2D(t_start, t_end)
    spline.addControlPoints([[3.0, 1.0], [5.0, 4.0], [2.0, 6.25], [6.0, 0.0], [8.0, 2.0], [10.0, -5.0]])

    x = []
    y = []
    for i in range(spline.getNumberOfSegments()):
        x_segment_values, y_segment_values = spline.evaluate(i)
        x.extend(x_segment_values)
        y.extend(y_segment_values)
    plt.figure()
    plt.plot(x, y)
    plt.plot(x_input, y_input, 'x')
    plt.show(block=False)

    plt.show()
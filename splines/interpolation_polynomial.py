import matplotlib.pyplot as plt
import numpy as np
import math

class InterpolationPolynomial:
    def __init__(self, control_points, t_start, t_end, compute_times=True):
        if compute_times:
            self.times = self._computeSegmentTimes(control_points, t_start, t_end)
        else:
            self.times = []
        self.control_points = control_points
        self.d = len(control_points)-1
        self.compute_times = compute_times

    def _computeSegmentTimes(self, control_points, start, end):
        total_time = end - start
        distances = []
        for i in range(len(control_points)-1):
            distance = control_points[i]-control_points[i+1]
            distance = math.sqrt(distance*distance)
            distances.append(distance)
        total_distance = sum(distances)
        segment_times = [value*total_time/total_distance for value in distances]
        times = [start]
        for segment_time in segment_times:
            times.append(times[-1] + segment_time)
        return times

    def setSegmentTimes(self, times):
        if not self.compute_times:
            self.times = times

    def _convexCombination(self, t, i, d):
        if d == 1:
            first = (self.times[i+1]-t)/(self.times[i+1]-self.times[i])*self.control_points[i]
            second = (t-self.times[i])/(self.times[i+1]-self.times[i])*self.control_points[i+1]
            return first + second
        first = (self.times[d+i] - t)/(self.times[d+i]-self.times[i])*self._convexCombination(t, i, d-1)
        second = (t - self.times[i])/(self.times[d+i]-self.times[i])*self._convexCombination(t, i+1, d-1)
        return first + second

    def evaluate(self, t):
        return self._convexCombination(t, 0, self.d)

class InterpolationPolynomial2D:
    def __init__(self, control_points=[], t_start=0.0, t_end=1.0):
        x_points, y_points = zip(*control_points)
        self.x = InterpolationPolynomial(x_points, t_start, t_end, False)
        self.y = InterpolationPolynomial(y_points, t_start, t_end, False)
        times = self._computeSegmentTimes(control_points, t_start, t_end)
        self.x.setSegmentTimes(times)
        self.y.setSegmentTimes(times)

    def _computeSegmentTimes(self, control_points, start, end):
        total_time = end - start
        distances = []
        for i in range(len(control_points)-1):
            distances.append(self._computeEuclideanNorm(control_points[i], control_points[i+1]))
        total_distance = sum(distances)
        segment_times = [value*total_time/total_distance for value in distances]
        times = [start]
        for segment_time in segment_times:
            times.append(times[-1] + segment_time)
        return times

    def _computeEuclideanNorm(self, first, second):
        x_dist = first[0] - second[0]
        y_dist = first[1] - second[1]
        return math.sqrt(x_dist*x_dist + y_dist*y_dist)

    def evaluate(self, t):
        return [self.x.evaluate(t), self.y.evaluate(t)]

if __name__ == '__main__':
    t_start = 0.0
    t_end = 5.0
    control_points = [1.0, -8.0, 4.0, 1.0, 8.0, 10.0, 1.25, -5.0, -10.0]
    poly = InterpolationPolynomial(control_points, t_start, t_end)
    times = np.linspace(t_start, t_end, 100)
    values = []
    for t in times:
        values.append(poly.evaluate(t))
    plt.figure()
    plt.plot(times, values)
    plt.plot(poly._computeSegmentTimes(control_points, t_start, t_end), control_points, 'x')
    plt.show(block=False)

    control_points = [[1.0, 2.0], [4.0, 2.5], [5.0, -0.0], [6.0, 4.0], [7.0, 10.0]]
    poly2d = InterpolationPolynomial2D(control_points, t_start, t_end)
    values2d = []
    for t in times:
        values2d.append(poly2d.evaluate(t))
    plt.figure()
    plt.plot(*zip(*values2d))
    plt.plot(*zip(*control_points), 'x')
    plt.show(block=False)

    plt.show()
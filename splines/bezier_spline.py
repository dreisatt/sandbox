import numpy as np
import matplotlib.pyplot as plt
import copy as cp

class BezierSpline:
    def __init__(self, start=0.0, end=1.0):
        self.control_points = []
        self.start_time = start
        self.end_time = end

    def addControlPoint(self, point):
        self.control_points.append(point)

    def addControlPoints(self, points):
        self.control_points = points

    def getNumControlPoints(self):
        return len(self.control_points)

    def _convexCombination(self, t, x, y):
        t = (t-self.start_time)/(self.end_time-self.start_time)
        return (1.0-t)*x + t*y

    def evaluate(self, t):
        if t >= self.start_time and t <= self.end_time:
            list = cp.deepcopy(self.control_points)
            # de Casteljau's algorithm
            for i in range(len(self.control_points)-1):
                for r in range(len(list)-1):
                    list[r] = self._convexCombination(t, list[r], list[r+1])
                del list[len(list)-1:]
            return list[0]
        else:
            print('Time t is too large or too small. Please check borders.')
            return 0.0

class BezierSpline2D:
    def __init__(self, start=0.0, end=1.0):
        self.x = BezierSpline(start, end)
        self.y = BezierSpline(start, end)
        self.control_points = []

    def addControlPoint(self, point):
        if len(point) == 2:
            self.x.addControlPoint(point[0])
            self.y.addControlPoint(point[1])
            self.control_points.append(point)
        else:
            raise TypeError("addControlPoint: control point does not have the proper dimension.")

    def addControlPoints(self, points):
        for point in points:
            self.addControlPoint(point)

    def evaluate(self, t):
        return [self.x.evaluate(t), self.y.evaluate(t)]

class BezierSpline3D:
    def __init__(self, start=0.0, end=1.0):
        self.x = BezierSpline(start, end)
        self.y = BezierSpline(start, end)
        self.z = BezierSpline(start, end)
        self.control_points = []

    def addControlPoints(self, points):
        for point in points:
            self.addControlPoint(point)

    def addControlPoint(self, point):
        if len(point) == 3:
            self.x.addControlPoint(point[0])
            self.y.addControlPoint(point[1])
            self.z.addControlPoint(point[2])
            self.control_points.append(point)
        else:
            raise TypeError("addControlPoint: control point does not have the proper dimension.")


    def evaluate(self, t):
        return [self.x.evaluate(t), self.y.evaluate(t), self.z.evaluate(t)]

if __name__ == "__main__":
    slow_spline2d = BezierSpline2D(0.0, 5.0)
    fast_spline2d = BezierSpline2D()
    control_points = [[-8.0, 0.0], [-5.0, 4.0], [-1.0, -1.0], [0.0, 0.0], [1.0, 4.5], [4.0,2.25], [6.0, 0.1], [8.0, -5.0]]
    slow_spline2d.addControlPoints(control_points)
    fast_spline2d.addControlPoints(control_points)
    slow_times = np.linspace(0.0, 5.0, 100)
    fast_times = np.linspace(0.0, 1.0, 100)
    slow_spline_values = [slow_spline2d.evaluate(t) for t in slow_times]
    fast_spline_values = [fast_spline2d.evaluate(t) for t in fast_times]

    plt.subplot(2, 1, 1)
    plt.plot(*zip(*control_points), 'ro')
    plt.plot(*zip(*slow_spline_values), 'g')
    plt.plot(*zip(*fast_spline_values), 'r')
    plt.title('X-Y spline data')
    plt.axis([-10.0, 10.0, -10.0, 10.0])
    plt.subplot(2, 1, 2)
    plt.plot(fast_times, list(zip(*fast_spline_values))[0], 'r')
    plt.plot(slow_times, list(zip(*slow_spline_values))[0], 'g')
    plt.title('X-coordinate over time')
    plt.axis([0.0, 10.0, -10.0, 10.0])

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(slow_times, *zip(*slow_spline_values), label='slow sline curve')
    ax.plot3D(fast_times, *zip(*fast_spline_values), 'g', label='fast spline curve' )
    plt.title('Spline points over time')
    ax.legend(loc=3)
    plt.show(block=False)

    spline3d = BezierSpline3D()
    control_points_3d = [[3.0, 1.0, 0.0], [5.0, 4.0, 2.0], [2.0, 6.25, 1.0], [6.0, 0.0, 2.0], [8.0, 2.0, 3.0], [10.0, -5.0, 1.0]]
    spline3d.addControlPoints(control_points_3d)
    spline3d_values = [spline3d.evaluate(t) for t in fast_times]

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(*zip(*spline3d_values), 'gray')
    ax.scatter3D(*zip(*control_points_3d))
    plt.show(block=False)

    plt.show()

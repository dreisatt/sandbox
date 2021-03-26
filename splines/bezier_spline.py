from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import copy as cp

class BezierSpline:

    def __init__(self, start = None, end = None):
        self.control_points = []
        if start is None and end is None:
            self.start_time = 0.0
            self.end_time = 1.0
        else:
            self.start_time = start
            self.end_time = end

    def addControlPoint(self, point):
        self.control_points.append(point)

    def addControlPoints(self, points):
        self.control_points = points

    def getNumControlPoints(self):
        return len(self.control_points)

    def convexCombination(self, t, x, y):
        t = (t-self.start_time)/(self.end_time-self.start_time)
        return (1.0-t)*x + t*y

    def evaluate(self, t):
        if t >= self.start_time and t <= self.end_time:
            list = cp.deepcopy(self.control_points)
            # de Casteljau's algorithm
            for i in range(0, len(self.control_points)-1):
                for r in range(0, len(list)-1):
                    list[r] = self.convexCombination(t, list[r], list[r+1])
                del list[len(list)-1:]
            return list[0]
        else:
            print('Time t is too large or too small. Please check borders.')
            return 0.0

class BezierSpline2D:

    def __init__(self, start = None, end = None):
        self.x = BezierSpline(start, end)
        self.y = BezierSpline(start, end)
        self.control_points = []

    def addControlPoint(self, point):
        if(point.shape[0] == 2):
            self.x.addControlPoint(point[0])
            self.y.addControlPoint(point[1])
            self.control_points.append(point)
        else:
            raise TypeError("addControlPoint: control point does not have the proper dimension.")

    def addControlPoints(self, points):
        for i in range(0, points.shape[0]):
            self.x.addControlPoint(points[i][0])
            self.y.addControlPoint(points[i][1])
            self.control_points.append(points[i])

    def evaluate(self, t):
        result = [self.x.evaluate(t), self.y.evaluate(t)]
        return result

if __name__ == "__main__":
    spline2d = BezierSpline2D(0.0, 5.0)
    spline2d_1 = BezierSpline2D()
#    control_points = np.array([[0.0, 0.0], [1.0, 4.5], [4.0,2.25]])
    control_points = np.array([[-8.0, 0.0], [-5.0, 4.0], [-1.0, -1.0], [0.0, 0.0], [1.0, 4.5], [4.0,2.25], [6.0, 0.1], [8.0, -5.0]])
    spline2d.addControlPoints(control_points)
    spline2d_1.addControlPoints(control_points)
    times = np.linspace(0.0, 5.0, 100)
    times_1 = np.linspace(0.0, 1.0, 100)
    result = [spline2d.evaluate(t) for t in times]
    result_1 = [spline2d_1.evaluate(t) for t in times_1]
    ## Plot result
    plt.subplot(2, 1, 1)
    plt.plot(control_points[:,0], control_points[:,1], 'ro')
    plt.plot(*zip(*result), 'g')
    plt.plot(*zip(*result_1), 'r')
    plt.title('X-Y spline data')
    plt.axis([-10.0, 10.0, -10.0, 10.0])
    plt.subplot(2, 1, 2)
    plt.plot(times_1, list(zip(*result_1))[0], 'r')
    plt.plot(times, list(zip(*result))[0], 'g')
    plt.title('X-coordinate over time')
    plt.axis([0.0, 10.0, -10.0, 10.0])
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot(times, *zip(*result), label='slow sline curve')
    ax.plot(times_1, *zip(*result_1), 'g', label='fast spline curve' )
    plt.title('Spline points over time')
    ax.legend(loc=3)
    plt.show()

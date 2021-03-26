from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
import copy as cp

class HermiteSpline:

    def __init__(self, control_points = None):
        self._control_points = control_points
        self._segments = []
        self.__H = np.matrix([[2.0, -2.0, 1.0, 1.0], [-3.0, 3.0, -2.0, -1.0], [0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0]])

    def Interpolate(self):
        for j in range(len(self._control_points)-1):
            derivative = self.FiniteDifference(self._control_points)
            G = np.array([self._control_points[j], self._control_points[j+1], derivative[j], derivative[j+1]]).reshape(4,1)
            self._segments.append(self.__H.dot(G))

    def Evaluate(self, time, segment):
        return (self.EvaluatePolynomial(t,3).dot(self._segments[segment])).flat[0]

    def EvaluatePolynomial(self, value, degree):
        T = np.array([])
        for i in range(degree, -1, -1):
            T = np.append(T, [value**i])
        return T.reshape(1, degree+1)

    def FiniteDifference(self, array):
        slope = [(array[1] - array[0])/2.0]
        for i in range(1, len(array)-1, +1):
            slope.append((array[i+1]-array[i-1])/2.0)
            slope.append((array[len(array)-1]-array[len(array)-2])/2.0)
        return slope

    def GetNumSegments(self):
        return len(self._control_points)-1

class HermiteSpline2D:

    def __init__(self, control_points = None):
        self.__x = HermiteSpline(control_points[0])
        self.__y = HermiteSpline(control_points[1])

    def Interpolate(self):
        self.__y.Interpolate()
        self.__x.Interpolate()

    def Evaluate(self, time, segment):
        return [self.__x.Evaluate(time, segment), self.__y.Evaluate(time, segment)]

    def NumSegments(self):
        return self.__x.GetNumSegments()

if __name__ == "__main__":
    Points = [[0.0, 3.0, 4.0, 5.0], [0.0, 2.0, 1.0, 1.25]]
    times = np.linspace(0.0, 1.0, num=1000)
    spline = HermiteSpline2D(Points)
    spline.Interpolate()
    values = [[], []]
    for j in range(spline.NumSegments()):
        for t in times:
            value = spline.Evaluate(t, j)
            values[0].append(value[0])
            values[1].append(value[1])
    plt.plot(Points[0], Points[1], 'ro')
    plt.plot(values[0], values[1], 'g')
    plt.show()
    # T = EvaluatePolynomial(2.0, 3)
    # H = np.matrix([[2.0, -2.0, 1.0, 1.0], [-3.0, 3.0, -2.0, -1.0], [0.0, 0.0, 1.0, 0.0], [1.0, 0.0, 0.0, 0.0]])
    # Results = []
    # for dim in range(len(Points)):
    #     values = Points[dim]
    #     result = []
    #     for j in range(len(values)-1):
    #         for t in times:
    #             derivative = FiniteDifference(values)
    #             G = np.array([values[j], values[j+1], derivative[j], derivative[j+1]]).reshape(4,1)
    #             result.append((EvaluatePolynomial(t,3).dot(H.dot(G))).flat[0])
    #     Results.append(result)
    # plt.plot(Points[0], Points[1], 'ro')
    # plt.plot(Results[0], Results[1], 'g')
    # plt.show()

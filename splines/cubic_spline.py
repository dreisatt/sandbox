import numpy as np
import math
from multipledispatch import dispatch

# p0(t) = c0 + c1*(t-t0) + c2*(t-t0)^2  + c3*(t-t0)^3
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
        self.number_segments = len(durations)-1
        self.polynomials = []
        if control_points == None:
            self.control_points = []
        else:
            self.control_points = control_points
            self._computeSplineCoefficient()
        self.segment = 0

    def getSegments(self):
        return self.number_segments

    def addControlPoints(self, control_points):
        self.control_points = control_points
        self._computeSplineCoefficient()

    @dispatch(float)
    def evaluate(self, t):
        # TODO::Niko: Implement binary search or something mapping from t to segment
        if t > self.durations[self.segment+1]:
            self.segment = self.segment + 1
        return self.polynomials[self.segment].evaluate(t)

    @dispatch(int)
    def evaluate(self, segment):
        if segment <= self.number_segments:
            times = np.linspace(self.durations[segment], self.durations[segment+1], 100)
            return times, self.polynomials[segment].evaluate(times)
        else:
            raise ValueError("Invalid segment id: ", segment)

    def _computeSplineCoefficient(self):
        A = np.zeros((4*self.number_segments, 4*self.number_segments))
        b = np.zeros((4*self.number_segments, 1))
        # First derivative equals zero at start and end of spline
        A[2][1] = 1.0
        A[3][(self.number_segments-1)*4+1] = 1.0
        delta = self.durations[-1]-self.durations[-2]
        A[3][(self.number_segments-1)*4+2] = 2.0*delta
        A[3][(self.number_segments-1)*4+3] = 3.0*delta*delta
        for i in range(self.number_segments):
            # Start of segment equals to boundary condition
            A[4*i][4*i] = 1.0
            b[4*i] = self.control_points[i]

            # End of segment equals to boundary condition
            A[4*i+1][4*i] = 1.0
            delta = self.durations[i+1]-self.durations[i]
            A[4*i+1][4*i+1] = delta
            A[4*i+1][4*i+2] = delta*delta
            A[4*i+1][4*i+3] = A[4*i+1][4*i+2] * delta
            b[4*i+1] = self.control_points[i+1]

            if i == 0:
                continue
            # First derivative condition (left hand side)
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
        x = x.reshape(self.number_segments, 4)
        for i in range(self.number_segments):
            self.polynomials.append(CubicPolynomial(x[i][0], x[i][1], x[i][2], x[i][3], self.durations[i]))

class CubicSpline2D:
    def __init__(self, t_start=0.0, t_end=1.0):
        self.t_start = t_start
        self.t_end = t_end

    def addControlPoints(self, control_points):
        durations = self._computeSegmentDuration(control_points)
        x = []
        y = []
        for point in control_points:
            x.append(point[0])
            y.append(point[1])
        self.xSpline = CubicSpline(durations)
        self.ySpline = CubicSpline(durations)
        self.xSpline.addControlPoints(x)
        self.ySpline.addControlPoints(y)

    def _computeSegmentDuration(self, control_points):
        total_time = self.t_end-self.t_start
        dist = []
        for i in range(len(control_points)-1):
            dist.append(self._computeNorm(control_points[i], control_points[i+1]))
        total_dist = sum(dist)
        # Normalize distance w.r.t. the total distance and time
        segment_durations = [item*total_time/total_dist for item in dist]
        durations = [self.t_start]
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

class CubicSpline3D:
    def __init__(self, t_start=0.0, t_end=1.0):
        self.control_points = []
        self.t_start = t_start
        self.t_end = t_end

    def addControlPoints(self, control_points):
        durations = self._computeSegmentDuration(control_points)
        x = []
        y = []
        z = []
        for point in control_points:
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        self.x_spline = CubicSpline(durations)
        self.y_spline = CubicSpline(durations)
        self.z_spline = CubicSpline(durations)
        self.x_spline.addControlPoints(x)
        self.y_spline.addControlPoints(y)
        self.z_spline.addControlPoints(z)

    def _computeSegmentDuration(self, control_points):
        total_time = self.t_end - self.t_start
        dist = []
        for i in range(len(control_points)-1):
            dist.append(self._computeNorm(control_points[i], control_points[i+1]))
        total_dist = sum(dist)
        segment_durations = [item*total_time/total_dist for item in dist]
        durations = [self.t_start]
        for segment_duration in segment_durations:
            durations.append(durations[-1] + segment_duration)
        return durations

    def _computeNorm(self, first, second):
        x_dist = first[0] - second[0]
        y_dist = first[1] - second[1]
        z_dist = first[2] - second[2]
        return math.sqrt(x_dist*x_dist + y_dist*y_dist + z_dist*z_dist)

    def evaluate(self, segment):
        tx, x = self.x_spline.evaluate(segment)
        ty, y = self.y_spline.evaluate(segment)
        tz, z = self.z_spline.evaluate(segment)
        return x, y, z

    def getNumberOfSegments(self):
        return self.x_spline.getSegments()

def fitCubicPolynomialWithMoments(points):
    # Number of points
    n = len(points)
    # Compute moments
    TriDiaMatrix = np.zeros(shape=(n,n), dtype=float)
    d = np.zeros(shape=(n,1), dtype=float)
    # Create moment matrix
    for i in range(0,n):
        # Check for end point conditions
        if(i == 0 or i == n-1):
            # Natural spline conditions
            TriDiaMatrix[i][i] = 2
            d[i][0] = 0
        else:
            h_i = points[i][0] - points[i-1][0]
            h_i_1 = points[i+1][0] - points[i][0]
            lambda_i = h_i_1/(h_i+h_i_1)
            mi_i = 1-lambda_i
            d_i = 6/(h_i+h_i_1)*((points[i+1][1]-points[i][1])/h_i_1 - (points[i][1]-points[i-1][1])/h_i)
            TriDiaMatrix[i][i-1] = mi_i
            TriDiaMatrix[i][i] = 2
            TriDiaMatrix[i][i+1] = lambda_i
            d[i][0] = d_i
    moments = np.linalg.solve(TriDiaMatrix, d)
    coefficients = []
    for i in range(0,n-1):
        a = points[i][1]
        h_i = (points[i+1][0]-points[i][0])
        b = (points[i+1][1]-points[i][1])/h_i - (2*moments[i]+moments[i+1])*h_i/6
        c = moments[i]/2
        d = (moments[i+1]-moments[i])/(6*h_i)
        coeff = np.array([a, b, c, d, points[i][0]], dtype=object)
        coefficients.append(coeff)
    return coefficients

def fitCubicPolynomial(points):
    # Number of polynomials
    n = len(points)-1
    A = np.zeros(shape=(4*n, 4*n), dtype=float)
    b = np.zeros(shape=(4*n, 1), dtype=float)

    # Iterate polynomial segments and add conditions to matrix
    for i in range(0, n):
        # Start point condition for polynomial segment
        A[i*4][i*4] = 1
        A[i*4][i*4+1] = points[i][0]-points[i][0]
        A[i*4][i*4+2] = (points[i][0]-points[i][0])**2
        A[i*4][i*4+3] = (points[i][0]-points[i][0])**3
        b[i*4] = points[i][1]

        # End point condition for polynomial segment
        A[i*4+1][i*4] = 1
        A[i*4+1][i*4+1] = points[i+1][0]-points[i][0]
        A[i*4+1][i*4+2] = (points[i+1][0]-points[i][0])**2
        A[i*4+1][i*4+3] = (points[i+1][0]-points[i][0])**3
        b[i*4+1] = points[i+1][1]

        if(i == 0):
            continue

        # First derivative condition (left hand side)
        A[i*4+2][(i-1)*4] = 0
        A[i*4+2][(i-1)*4+1] = 1
        A[i*4+2][(i-1)*4+2] = 2*(points[i][0]-points[i-1][0])
        A[i*4+2][(i-1)*4+3] = 3*(points[i][0]-points[i-1][0])**2
        # First derivative condition (right hand side)
        A[i*4+2][i*4] = 0
        A[i*4+2][i*4+1] = -1
        A[i*4+2][i*4+2] = -2*(points[i][0]-points[i][0])
        A[i*4+2][i*4+3] = -3*(points[i][0]-points[i][0])**2
        # Second derivative condition (left hand side)
        A[i*4+3][(i-1)*4] = 0
        A[i*4+3][(i-1)*4+1] = 0
        A[i*4+3][(i-1)*4+2] = 2
        A[i*4+3][(i-1)*4+3] = 6*(points[i][0]-points[i-1][0])
        # Second derivative condition (right hand side)
        A[i*4+3][i*4] = 0
        A[i*4+3][i*4+1] = 0
        A[i*4+3][i*4+2] = -2
        A[i*4+3][i*4+3] = -6*(points[i][0]-points[i][0])
    # Additional conditions on start and end segment
    A[2][2] = 2
    A[2][3] = 6*(points[0][0]-points[0][0])
    A[3][(n-1)*4+2] = 2
    A[3][(n-1)*4+3] = 6*(points[n][0]-points[n-1][0])
    x = np.linalg.solve(A, b)
    coeff = x.reshape(n,4)
    return coeff

def cubicPolynomial(x, shift, coeff):
    return coeff[0] + coeff[1]*(x-shift) + coeff[2]*(x-shift)**2 + coeff[3]*(x-shift)**3

def cubicPolyFirstDerivative(x, shift, coeff):
    return coeff[1] + 2*coeff[2]*(x-shift) + 3*coeff[3]*(x-shift)**2

def cubicPolySecondDerivative(x, shift, coeff):
    return 2*coeff[2] + 6*coeff[3]*(x-shift)

def computeSplinePoints(x_points, control_points, spline_coeffients):
    result = []
    control_counter = 1
    for i in range(0, len(x_points)):
        if(x_points[i] < control_points[control_counter][0]):
            result.append(cubicPolynomial(x_points[i], control_points[control_counter-1][0], spline_coeffients[control_counter-1]))
        else:
            if(control_counter < len(control_points)-1):
                control_counter = control_counter+1
            result.append(cubicPolynomial(x_points[i], control_points[control_counter-1][0], spline_coeffients[control_counter-1]))
    return result
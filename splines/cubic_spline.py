import numpy as np
from scipy import interpolate
import random as rd
import matplotlib.pyplot as plt

def sciCubicSpline(x, y, order):
    coeff = interpolate.splrep(x,y,k=order)
    return coeff

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
#    print(TriDiaMatrix)
#    print(d)
    moments = np.linalg.solve(TriDiaMatrix, d)
#    print(moments)
    coefficients = []
    for i in range(0,n-1):
        a = points[i][1]
        h_i = (points[i+1][0]-points[i][0])
        b = (points[i+1][1]-points[i][1])/h_i - (2*moments[i]+moments[i+1])*h_i/6
        c = moments[i]/2
        d = (moments[i+1]-moments[i])/(6*h_i)
        coeff = np.array([a, b, c, d, points[i][0]])
        coefficients.append(coeff)
    return coefficients

def fitCubicPolynomial(points):
    # Number of polynomials
    n = len(points)-1
    print(n)
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
    print(A)
    print(b)
#    print(A.shape)
    x = np.linalg.solve(A, b)
#    print(x)
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


if __name__ == "__main__":
    c_x = [1.0, 3.0, 4.0, 5.0, 6.0]
    c_y = [1.0, 1.0, 0.25, 0.2, 1.0/6.0]
    sci_coeffients = sciCubicSpline(c_x, c_y, 3)
    #print(sci_coeffients)
    # Control point array (y=f(x)=1/x)
    c0 = np.array([1.0, 1.0])
    c1 = np.array([2.0, 3.0])
    c2 = np.array([3.0, 2.25])
    c3 = np.array([5.0, 0.2])
    c4 = np.array([6.0, 1.0/6.0])
    control_points = [c0, c1, c2, c3, c4]
    new_spline = fitCubicPolynomialWithMoments(control_points)
    # Compute polynomial coeffients
    spline_coeffients = fitCubicPolynomial(control_points)
    # Compute interpolation values
    x_values = np.linspace(control_points[0][0], control_points[len(control_points)-1][0], num=10000)
    control_counter = 1
    result = []
    for i in range(0, x_values.size):
        if(x_values[i] < control_points[control_counter][0]):
            result.append(cubicPolynomial(x_values[i], control_points[control_counter-1][0], spline_coeffients[control_counter-1]))
        else:
            if(control_counter < len(control_points)-1):
                control_counter = control_counter+1
            result.append(cubicPolynomial(x_values[i], control_points[control_counter-1][0], spline_coeffients[control_counter-1]))
    new_result = []
    control_counter = 1
    for i in range(0, x_values.size):
        if(x_values[i] < control_points[control_counter][0]):
            new_result.append(cubicPolynomial(x_values[i], new_spline[control_counter-1][4], new_spline[control_counter-1]))
        else:
            if(control_counter < len(control_points)-1):
                control_counter = control_counter+1
            new_result.append(cubicPolynomial(x_values[i], new_spline[control_counter-1][4], new_spline[control_counter-1]))
    # Compare results
    #sciResult = []
    #for x in x_values:
    #    sciResult.append(interpolate.splev(x, sci_coeffients))
    #x_points = [1.5117349624633789,
    #2.0380945205688477,
    #2.5683050155639648,
    #3.0485596656799316,
    #3.4642939567565918,
    #3.890139102935791,
    #4.3982338905334473,
    #4.9317374229431152,
    #5.466315746307373]
    #y_points = []
    #control_counter = 1
    #for i in range(0, len(x_points)):
    #    if(x_points[i] < control_points[control_counter][0]):
    #        y_points.append(cubicPolynomial(x_points[i], control_points[control_counter-1][0], spline_coeffients[control_counter-1]))
    #    else:
    #        if(control_counter < len(control_points)-1):
    #            control_counter = control_counter+1
    #        y_points.append(cubicPolynomial(x_points[i], control_points[control_counter-1][0], spline_coeffients[control_counter-1]))
    # Plot interpolation
    plt.plot(x_values, result, 'r')
    for point in control_points:
        plt.plot(point[0], point[1], 'x')
    plt.plot(x_values, new_result, 'g')
    #plt.plot(x_points, y_points, 'o')
    plt.show()

import numpy as np
import matplotlib.pyplot as plt
from cubic_spline import CubicSpline, CubicSpline2D, CubicSpline3D
from cubic_spline import segmentTimes
from cubic_spline import fitCubicPolynomial, fitCubicPolynomialWithMoments, cubicPolynomial

if __name__=='__main__':
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
    plt.figure()
    plt.plot(x_values, result, 'r')
    for point in control_points:
        plt.plot(point[0], point[1], 'x')
    plt.plot(x_values, new_result, 'g')
    plt.show(block=False)

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

    xy_spline = CubicSpline2D(t_start, t_end)
    xy_spline.addControlPoints([[3.0, 1.0], [5.0, 4.0], [2.0, 6.25], [6.0, 0.0], [8.0, 2.0], [10.0, -5.0]])

    x = []
    y = []
    for i in range(xy_spline.getNumberOfSegments()):
        x_segment_values, y_segment_values = xy_spline.evaluate(i)
        x.extend(x_segment_values)
        y.extend(y_segment_values)
    plt.figure()
    plt.plot(x, y)
    plt.plot(x_input, y_input, 'x')
    plt.show(block=False)

    xyz_spline = CubicSpline3D(t_start, t_end)
    x_input, y_input, z_input = xyz_spline.addControlPoints([[3.0, 1.0, 0.0], [5.0, 4.0, 2.0], [2.0, 6.25, 1.0], [6.0, 0.0, 2.0], [8.0, 2.0, 3.0], [10.0, -5.0, 1.0]])

    x = []
    y = []
    z = []

    for i in range(xyz_spline.getNumberOfSegments()):
        x_segment_values, y_segment_values, z_segment_values = xyz_spline.evaluate(i)
        x.extend(x_segment_values)
        y.extend(y_segment_values)
        z.extend(z_segment_values)

    plt.figure()
    ax = plt.axes(projection='3d')
    ax.plot3D(x, y, z, 'gray')
    ax.scatter3D(x_input, y_input, z_input)
    plt.show(block=False)

    plt.show()
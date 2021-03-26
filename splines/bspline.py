#!/usr/bin/python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

def findSpan(degree, knot, knot_vector):
    n = len(knot_vector)-degree-1
    if knot == knot_vector[n+1]:
        return n
    else:
        low = degree
        high = n+1
        mid = (low + high)//2
        while (knot < knot_vector[mid]) or (knot > knot_vector[mid+1]):
            if knot < knot_vector[mid]:
                high = mid
            else:
                low = mid
            mid = (low + high)//2
        return mid

# Global data
degree = 3
data = np.array([[3, 2], [4, 5], [5, 3]])
# Compute interpolation points
t = np.linspace(0.0, 1.0, num=100)

# Compute knot vector
knots_size = degree + data.shape[0] + 1
clamped = True
knots = np.zeros(knots_size)
if (clamped):
    for i in range(degree):
        np.append(knots, 1.0)

i = findSpan(2, 2.5, [0, 0, 0, 1, 2, 3, 4, 4, 5, 5, 5])
print("Index: " + str(i))

# Visualization
plt.plot(data[:,0], data[:,1], 'ro')
plt.show()

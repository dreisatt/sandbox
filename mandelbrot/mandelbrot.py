import numpy as np
from matplotlib import pyplot as plt
import matplotlib
import sys
from PIL import Image

numberOfIterations = 100
radius = 2.4

rows = 1080
cols = 1920

real_max = 0.5
real_min = -1.5

im_max = 1.0
im_min = -0.5

def MapPixelToComplex(m, n) -> complex:
    real = ((real_max-real_min)/(cols-1)) * m + real_min
    imag = ((im_max-im_min)/(rows-1)) * n + im_min
    return complex(real, imag)

def IsInMandelBrotSet(c):
    z = complex(0.0, 0.0)
    for i in range(numberOfIterations):
        z = z**2 + c
        if abs(z) > radius:
            return False, i
    return True, numberOfIterations

img = np.full((rows, cols, 3), [0, 100, 0], dtype=np.uint8)
for i in range(cols):
    for j in range(rows):
        c = MapPixelToComplex(i, j)
        inside, it = IsInMandelBrotSet(c)
        if inside:
            img[j,i] = [255, 0, 0]
        else:
            img[j,i] = [0, 155+it, 0]

im = Image.fromarray(img).convert("RGB")
im.save("/tmp/mandelbrot.jpeg")
matplotlib.use("GTK3Cairo")
plt.imshow(img)
plt.show()
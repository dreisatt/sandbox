import numpy as np
import math as math
import matplotlib.pyplot as plt

def computeLookUpTable(func, start:float, end: float, amount: int):
    delta = (end-start)/float(amount-1)
    # Compute midpoints of interval
    samples = [start + delta/2.0]
    for i in range(1, amount-1):
        samples.append(samples[0]+float(i)*delta)
    table = func(samples)
    def lookUpTable(x):
        if x < end and x > start:
            i = math.floor((float(x)-start)/delta)
            return table[i]
        else:
            raise RuntimeError("lookUpValue: value {value} is not within range ]{begin},...,{final}[".format(value=x, begin=start, final=end))
    return lookUpTable

def computeLookUpTableInterpolation(func, start: float, end: float, amount: int):
    delta = (end-start)/float(amount)
    samples = []
    # Compute endpoints of intervals
    for i in range(0, (amount+1)):
        samples.append(float(i)*delta+start)
    # Evaluate func at the endpoints
    table = func(samples)
    def lookUpTable(x: float):
        if x < end and x > start:
            ii = (float(x)-start)/delta
            i = math.floor(ii)
            if i == amount:
                i = amount-1
            u = ii-i
            # Linear interpolate between neighboring intervals
            return table[i]*(1-u) + u*table[i+1]
        else:
            raise RuntimeError("lookUpValue: value {value} is not within range ]{begin},...,{final}[".format(value=x, begin=start, final=end))
    return lookUpTable

if __name__ == '__main__':
    start = 0.2
    end = 5.0
    number_samples = 32

    lookUpSqrt = computeLookUpTable(np.sqrt, start, end, number_samples)
    lookUpLog = computeLookUpTableInterpolation(np.log, start, end, number_samples)
    xs = np.linspace(start+0.1, end-0.1, 1000)
    try:
        approx_sqrt_ys = [lookUpSqrt(x) for x in xs]
        approx_log_ys = [lookUpLog(x) for x in xs]
        sqrt_ys = np.sqrt(xs)
        log_ys = np.log(xs)

        error_sqrt = [exact-approx for exact, approx  in zip(sqrt_ys, approx_sqrt_ys)]
        error_log = [exact-approx for exact, approx in zip(log_ys, approx_log_ys)]

        total_sqrt_error = 0.0
        for element in error_sqrt:
            total_sqrt_error = total_sqrt_error + abs(element)
        total_sqrt_error = total_sqrt_error/len(error_sqrt)
        print("Total error of sqrt approximation: ", total_sqrt_error)

        plt.figure()
        plt.plot(xs, sqrt_ys)
        plt.plot(xs, log_ys)
        plt.plot(xs, approx_sqrt_ys)
        plt.plot(xs, approx_log_ys)
        plt.show(block=False)

        plt.figure()
        plt.plot(xs, error_sqrt)
        # plt.plot(xs, error_log)
        plt.show(block=False)
        plt.show()
    except RuntimeError as e:
        print(e)



import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter
import scipy.stats

"""
0) read each value. sum average forces for each displacement
1) get average values and uncertainty for each point
2) plot each point
3) draw best-fit line
"""

VOLTAGE_INSTRUMENTAL_UNCERTAINTY_FACTOR = 0.05
AXES_DECIMAL_POINTS = 3

class DokiAvgPoint:
    def __init__(self, insError):
        self.n = 0
        self.sum = 0.0
        self.l = None
        self.h = None
        self.insError = insError

    def add(self, val):
        self.n += 1
        self.sum += val

        if self.l == None:
            self.l = val
        if self.h == None:
            self.h = val

        self.l = min(self.l, val)
        self.h = max(self.h, val)

    def avg(self):
        if self.n == 0:
            return 0.0

        return self.sum / self.n

    def error(self):
        if self.n == 0:
            return self.insError
        avg = self.avg()
        owo = abs(avg - self.h)
        uwu = abs(avg - self.l)
        return max(max(owo, uwu), self.insError)

    def __str__(self):
        return "N=%d, sum=%.3f, range=[%.3f, %.3f], error=%.3f, avg=%.3f" % (self.n, self.sum, self.l, self.h, self.error(), self.avg())
    
avgPts = {}

with open('B3Data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r = 1 / float(row['xR'])
        v = 1 / float(row['V'])
        rStr = str(r)
        if not rStr in avgPts:
            avgPts[rStr] = DokiAvgPoint(VOLTAGE_INSTRUMENTAL_UNCERTAINTY_FACTOR * v)
        avgPts[rStr].add(v)

axisFormat = FormatStrFormatter("%%.%df" % AXES_DECIMAL_POINTS)

def drawGraph(title):
    print("Drawing Graph: \"%s\"" % title)
    plt.title(title)
    plt.ylabel("Inverse of test voltage (V^-1)")
    plt.xlabel("Inverse of test resistance (Ω^-1)")

    gca = plt.gca()
    gca.yaxis.set_major_formatter(axisFormat)
    gca.xaxis.set_major_formatter(axisFormat)

    xArr = []
    yArr = []

    for rStr in avgPts:
        r = float(rStr)
        dap = avgPts[rStr]

        x = r
        y = dap.avg()
        xArr.append(x)
        yArr.append(y)

        print("(%.3f, %.3f), error=%.3f" % (x, y, dap.error()))
        plt.scatter(x, y)
        plt.errorbar(x, y, yerr=dap.error(), fmt='--o', barsabove=True, capsize=8)

    npXarr = np.array(xArr)
    npYarr = np.array(yArr)

    m, b, r_value, p_value, std_err = scipy.stats.linregress(npXarr, npYarr)
    rS = r_value ** 2
    print("BestFit: m=%.3f, b=%.3f, rSqrd=%.3f" % (m, b, rS))
    xmin, xmax = gca.get_xlim()
    plt.axline((xmin, (m * xmin) + b), (xmax, (m * xmax) + b))
    plt.show()
    print("------\n")


drawGraph("Inv. of test voltage vs Inv. of test resistance")
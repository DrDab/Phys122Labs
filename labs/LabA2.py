import csv
import matplotlib.pyplot as plt
import numpy as np
import math

"""
0) read each value. sum average forces for each displacement
1) get average values and uncertainty for each point
2) plot each point
3) draw best-fit line
"""

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

FORCE_INSTRUMENTAL_UNCERTAINTY = 0.005

with open('A2Data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r = float(row['Separation'])
        f = float(row['Force'])
        rStr = str(r)
        if not rStr in avgPts:
            avgPts[rStr] = DokiAvgPoint(FORCE_INSTRUMENTAL_UNCERTAINTY)
        avgPts[rStr].add(f)


plt.title("Graph1")
plt.ylabel("Force (N), +/- %.3f N" % FORCE_INSTRUMENTAL_UNCERTAINTY)
plt.xlabel("Inverse-%s of Separation (m^%d)" % ("square", -2))

xArr = []
yArr = []

for rStr in avgPts:
    r = float(rStr)
    dap = avgPts[rStr]

    x = r ** -2
    y = dap.avg()
    xArr.append(x)
    yArr.append(y)

    print("Plotting Point: %s" % dap)
    print("@(%.3f, %.3f)" % (x, y))
    plt.scatter(x, y)
    plt.errorbar(x, y, yerr=dap.error(), fmt='--o', barsabove=True, capsize=8)

m, b = np.polyfit(np.array(xArr), np.array(yArr), 1)
print("BestFit: m=%.3f, b=%.3f" % (m, b))
xmin, xmax = plt.gca().get_xlim()
plt.axline((xmin, (m * xmin) + b), (xmax, (m * xmax) + b))
plt.show()
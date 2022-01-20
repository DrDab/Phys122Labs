import csv
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import FormatStrFormatter

"""
0) read each value. sum average forces for each displacement
1) get average values and uncertainty for each point
2) plot each point
3) draw best-fit line
"""

FORCE_INSTRUMENTAL_UNCERTAINTY = 0.005

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

with open('A2Data.csv') as f:
    reader = csv.DictReader(f)
    for row in reader:
        r = float(row['Separation'])
        f = float(row['Force'])
        rStr = str(r)
        if not rStr in avgPts:
            avgPts[rStr] = DokiAvgPoint(FORCE_INSTRUMENTAL_UNCERTAINTY)
        avgPts[rStr].add(f)

axisFormat = FormatStrFormatter("%.3f")

def drawGraph(title, sepTxt, pow):
    print("Drawing Graph: \"%s\"" % title)
    plt.title(title)
    plt.ylabel("Force (N), +/- %.3f N" % FORCE_INSTRUMENTAL_UNCERTAINTY)
    plt.xlabel("%sseparation (m^%d)" % (sepTxt, pow))

    gca = plt.gca()
    gca.yaxis.set_major_formatter(axisFormat)
    gca.xaxis.set_major_formatter(axisFormat)

    xArr = []
    yArr = []

    for rStr in avgPts:
        r = float(rStr)
        dap = avgPts[rStr]

        x = r ** pow
        y = dap.avg()
        xArr.append(x)
        yArr.append(y)

        print("Plotting Point: %s" % dap)
        print("@(%.3f, %.3f)" % (x, y))
        plt.scatter(x, y)
        plt.errorbar(x, y, yerr=dap.error(), fmt='--o', barsabove=True, capsize=8)

    m, b = np.polyfit(np.array(xArr), np.array(yArr), 1)
    print("BestFit: m=%.3f, b=%.3f" % (m, b))
    xmin, xmax = gca.get_xlim()
    plt.axline((xmin, (m * xmin) + b), (xmax, (m * xmax) + b))
    plt.show()
    plt.savefig('filename.png', dpi=300)
    print("------\n")

drawGraph("E-Force vs. charge separation", "", 1)
drawGraph("E-Force vs. Inv. of charge separation", "inverse of ", -1)
drawGraph("E-Force vs. Inv. Sqr of charge separation", "inverse-square of ", -2)
drawGraph("E-Force vs. Inv. Cube of charge separation", "inverse-cube of ", -3)
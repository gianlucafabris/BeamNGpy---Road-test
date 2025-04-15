import pandas as pd
import csv
import random

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from settings_utility import *

file_csv = "results_3points.csv"
result = None

def calcRadius(row, debug=False):
    lenght1, angle1, lenght2, angle2, res = row
    p_x = []
    p_y = []
    xo, yo, x, y, x2, y2 = to3points(0, 0, lenght1, 0, lenght2, angle2)
    p_x, p_y = np.append(p_x, xo), np.append(p_y, yo) #1 point
    p_x, p_y = np.append(p_x, x), np.append(p_y, y) #2 point
    p_x, p_y = np.append(p_x, x2), np.append(p_y, y2) #3 point
    #fix - put point to derive at top/bottom
    p_x, p_y = applyRotationArray((p_x, p_y), math.radians(-angle2/2))
    #radius
    x = p_x[1]
    r = radiusCurvature(p_x, p_y, x)
    if debug:
        visualizeCatmullrom(p_x, p_y)
    return round(r, 3)

def addRadius(debug=False):
    global result
    global file_csv
    if "radius1" not in result.columns:
        result["radius1"] = result.apply(calcRadius, axis=1, args=[debug])
        result.to_csv(file_csv, index=False)

def visualize():
    global result
    fig, ax = plt.subplots()
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, res, radius1 = row
        rnd = random.random() - 0.5
        if res == 1:
            ax.scatter(radius1, rnd, color="green")
        elif res == 2:
            ax.scatter(radius1, rnd, color="blue")
        else:
            ax.scatter(radius1, rnd, color="red")
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlabel('radius')
    ax.set_title('3 points - radius')
    plt.show()

    fig, ax = plt.subplots()
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, res, radius1 = row
        rnd = random.random() - 0.5
        if res == 1:
            ax.scatter(radius1, rnd, color="green")
        elif res == 2:
            ax.scatter(radius1, rnd, color="blue")
        else:
            ax.scatter(radius1, rnd, color="red")
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.set_xlabel('radius log')
    ax.set_title('3 points - radius')
    ax.set_xscale("log")
    plt.show()

def analysis():
    global result
    print("indices\n", result.describe(), sep="")
    print("correlation\n", result.corr(), sep="")

def main():
    global file_csv
    global result
    result = pd.read_csv(file_csv)
    addRadius()
    visualize()
    analysis()

if __name__ == '__main__':
    main()

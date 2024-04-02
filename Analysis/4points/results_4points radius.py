import pandas as pd
import csv

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from settings_utility import *

file_csv = "results_4points.csv"
result = None

def calcRadius(row, index, debug=False):
    if index==1:
        lenght1, angle1, lenght2, angle2, lenght3, angle3, res = row
    else:
        lenght1, angle1, lenght2, angle2, lenght3, angle3, res, radius1 = row
    p_x = []
    p_y = []
    xo, yo, x, y, x2, y2, x3, y3 = to4points(0, 0, lenght1, 0, lenght2, angle2, lenght3, angle3)
    p_x, p_y = np.append(p_x, xo), np.append(p_y, yo) #1 point
    p_x, p_y = np.append(p_x, x), np.append(p_y, y) #2 point
    p_x, p_y = np.append(p_x, x2), np.append(p_y, y2) #3 point
    p_x, p_y = np.append(p_x, x3), np.append(p_y, y3) #4 point
    #fix - put point to derive at top/bottom
    if index == 1:
        p_x, p_y = applyRotationArray((p_x, p_y), math.radians(-angle2/2))
        x = p_x[1]
    else:
        p_x, p_y = applyRotationArray(applyRotationArray((p_x, p_y), math.radians(-angle3/2)), math.radians(-angle2))
        x = p_x[2]
    #radius
    r = radiusCurvature(p_x, p_y, x)
    if debug:
        visualizeCatmullrom(p_x, p_y)
    return round(r, 3)

def addRadius(debug=False):
    global result
    glbal file_csv
    if "radius1" not in result.columns:
        result["radius1"] = result.apply(calcRadius, axis=1, args=[1, debug])
        result["radius2"] = result.apply(calcRadius, axis=1, args=[2, debug])
        result.to_csv(file_csv, index=False)

def visualize():
    global result
    fig, ax = plt.subplots()
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, lenght3, angle3, res, radius1, radius2 = row
        if res == 1:
            ax.scatter(radius1, radius2, color="green")
        elif res == 2:
            ax.scatter(radius1, radius2, color="blue")
        else:
            ax.scatter(radius1, radius2, color="red")
    ax.set_xlabel('radius')
    ax.set_ylabel('radius2')
    ax.set_title('4 points - radius')
    plt.show()

    fig, ax = plt.subplots()
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, lenght3, angle3, res, radius1, radius2 = row
        if res == 1:
            ax.scatter(radius1, radius2, color="green")
        elif res == 2:
            ax.scatter(radius1, radius2, color="blue")
        else:
            ax.scatter(radius1, radius2, color="red")
    ax.set_xlabel('radius log')
    ax.set_ylabel('radius2 log')
    ax.set_title('4 points - radius')
    ax.set_xscale("log")
    ax.set_yscale("log")
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

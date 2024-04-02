import pandas as pd
import csv

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from settings_utility import *

file_csv = "results_5points.csv"
result = None

def calcRadius(row, index, debug=False):
    if index == 1:
        lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4, res = row
    elif index == 2:
        lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4, res, radius1 = row
    else:
        lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4, res, radius1, radius2 = row
    p_x = []
    p_y = []
    xo, yo, x, y, x2, y2, x3, y3, x4, y4 = to4points(0, 0, lenght1, 0, lenght2, angle2, lenght3, angle3, lenght4, angle4)
    p_x, p_y = np.append(p_x, xo), np.append(p_y, yo) #1 point
    p_x, p_y = np.append(p_x, x), np.append(p_y, y) #2 point
    p_x, p_y = np.append(p_x, x2), np.append(p_y, y2) #3 point
    p_x, p_y = np.append(p_x, x3), np.append(p_y, y3) #4 point
    p_x, p_y = np.append(p_x, x4), np.append(p_y, y4) #5 point
    #fix - put point to derive at top/bottom
    if index == 1:
        p_x, p_y = applyRotationArray((p_x, p_y), math.radians(-angle2/2))
        x = p_x[1]
    elif index == 2:
        p_x, p_y = applyRotationArray(applyRotationArray((p_x, p_y), math.radians(-angle3/2)), math.radians(-angle2))
        x = p_x[2]
    else:
        p_x, p_y = applyRotationArray(applyRotationArray((applyRotationArray((p_x, p_y), math.radians(-angle4/2))), math.radians(-angle3)), math.radians(-angle2))
        x = p_x[3]
    #radius
    r = radiusCurvature(p_x, p_y, x)
    if debug:
        visualizeCatmullrom(p_x, p_y)
    return round(r, 3)

def addRadius(debug=False):
    global result
    global file_csv
    if "radius1" not in result.columns:
        result["radius1"] = result.apply(calcRadius, axis=1, args=[1, debug])
        result["radius2"] = result.apply(calcRadius, axis=1, args=[2, debug])
        result["radius3"] = result.apply(calcRadius, axis=1, args=[3, debug])
        result.to_csv(file_csv, index=False)

def visualize():
    global result
    for f in range(4):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        for row in result.itertuples(index=False):
            lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4, res, radius1, radius2, radius3 = row
            if res == 1:
                ax.scatter(radius1, radius2, radius3, color="green")
            elif res == 2:
                ax.scatter(radius1, radius2, radius3, color="blue")
            else:
                ax.scatter(radius1, radius2, radius3, color="red")
        ax.set_xlabel('radius')
        ax.set_ylabel('radius2')
        ax.set_zlabel('radius3')
        ax.set_title('5 points - radius')
        if f==1:
            ax.view_init(elev=90, azim=-90)
        elif f==2:
            ax.view_init(elev=0, azim=-90)
        elif f==3:
            ax.view_init(elev=0, azim=0)
        plt.show()

    for f in range(4):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        for row in result.itertuples(index=False):
            lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4, res, radius1, radius2, radius3 = row
            if radius1 == 0:
                radius1 = 10**-6
            if radius2 == 0:
                radius2 = 10**-6
            if radius3 == 0:
                radius3 == 10**-6
            r1l = math.log(radius1)
            r2l = math.log(radius2)
            r3l = math.log(radius3)
            if res == 1:
                ax.scatter(r1l, r2l, r3l, color="green")
            elif res == 2:
                ax.scatter(r1l, r2l, r3l, color="blue")
            else:
                ax.scatter(r1l, r2l, r3l, color="red")
        ax.set_xticklabels([f"{10**int(t.get_text().replace('−', '-')):.0e}" for t in ax.get_xticklabels()])
        ax.set_yticklabels([f"{10**int(t.get_text().replace('−', '-')):.0e}" for t in ax.get_yticklabels()])
        ax.set_zticklabels([f"{10**int(t.get_text().replace('−', '-')):.0e}" for t in ax.get_zticklabels()])
        ax.set_xlabel('radius log')
        ax.set_ylabel('radius2 log')
        ax.set_zlabel('radius3 log')
        ax.set_title('5 points - radius')
        #not working with scale log (works with data log)
        # ax.set_xscale("log")
        # ax.set_yscale("log")
        # ax.set_zscale("log")
        if f==1:
            ax.view_init(elev=90, azim=-90)
        elif f==2:
            ax.view_init(elev=0, azim=-90)
        elif f==3:
            ax.view_init(elev=0, azim=0)
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

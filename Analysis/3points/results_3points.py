import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from test_analysis import *
from settings_utility import *

file_csv = "results_3points.csv"
result = None

def visualize():
    global result
    for f in range(4):
        fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
        i = -1
        i2 = -1
        j2 = -1
        lenght1_old = ""
        lenght2_old = ""
        for row in result.itertuples(index=False):
            lenght1, angle1, lenght2, angle2, res, radius1 = row
            if lenght1 != lenght1_old:
                lenght1_old = lenght1
                i += 1
                i2 = -1
                j2 = -1
            if lenght2 != lenght2_old:
                lenght2_old = lenght2
                i2 += 1
                j2 = -1
            j2 += 1
            if res == 1:
                ax.scatter(j2, i2, i, color="green")
            elif res == 2:
                ax.scatter(j2, i2, i, color="blue")
            # else:
            #     ax.scatter(j2, i2, i, color="red")
        x = result["angle2"].unique()
        y = result["lenght2"].unique()
        z = result["lenght1"].unique()
        ax.set_xticks(range(len(x)))
        ax.set_xticklabels(x)
        ax.set_yticks(range(len(z)))
        ax.set_yticklabels(z)
        ax.set_zticks(range(len(y)))
        ax.set_zticklabels(y)
        ax.set_xlabel('angle2')
        ax.set_ylabel('lenght2')
        ax.set_zlabel('lenght')
        ax.set_title('3 points')
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
    #creating one long road merging all tests
    nodes = []
    prev_point = [0,0]
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, res, radius1 = row
        xo, yo, x, y, x2, y2 = to3points(prev_point[0], prev_point[1], lenght1, angle1, lenght2, angle2)
        nodes.append([x,y])
        nodes.append([x2,y2])
        prev_point = [x2,y2]
    _, dir_coverage = direction_coverage(nodes, 36, True)
    print("direction coverage\n", round(dir_coverage*100, 3), "%", sep="")

def main():
    global file_csv
    global result
    result = pd.read_csv(file_csv)
    visualize()
    analysis()

if __name__ == '__main__':
    main()

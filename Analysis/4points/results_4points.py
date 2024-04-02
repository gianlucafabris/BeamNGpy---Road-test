import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from test_analysis import *
from settings_utility import *

file_csv = "results_4points.csv"
result = None

def visualize():
    global result
    for f in range(4):
        a = result["lenght2"].unique()
        b = result["lenght1"].unique()
        fig, axs = plt.subplots(len(b), len(a), subplot_kw={"projection": "3d"})
        i = 0
        while i < len(b):
            i2 = 0
            while i2 < len(a):
                j2 = -1
                i3 = -1
                j3 = -1
                angle2_old = ""
                lenght3_old = ""
                for row in result.itertuples(index=False):
                    lenght1, angle1, lenght2, angle2, lenght3, angle3, res, radius1, radius2 = row
                    if lenght1 == b[i] and lenght2 == a[i2]:
                        if angle2 != angle2_old:
                            angle2_old = angle2
                            j2 += 1
                            i3 = -1
                            j3 = -1
                        if lenght3 != lenght3_old:
                            lenght3_old = lenght3
                            i3 += 1
                            j3 = -1
                        j3 += 1
                        if res == 1:
                            axs[i,i2].scatter(j3, i3, j2, color="green")
                        elif res == 2:
                            axs[i,i2].scatter(j3, i3, j2, color="blue")
                        # else:
                        #     axs[i,i2].scatter(j3, i3, j2, color="red")
                x = result["angle3"].unique()
                y = result["lenght3"].unique()
                z = result["angle2"].unique()
                axs[i,i2].set_xticks(range(len(x)))
                axs[i,i2].set_xticklabels(x)
                axs[i,i2].set_yticks(range(len(y)))
                axs[i,i2].set_yticklabels(y)
                axs[i,i2].set_zticks(range(len(z)))
                axs[i,i2].set_zticklabels(z)
                axs[i,i2].set_xlabel('angle3')
                axs[i,i2].set_ylabel('lenght3')
                axs[i,i2].set_zlabel('angle2')
                #axs[i,i2].set_title(f"lenght={b[i]} lenght2={a[i2]}")
                if f==1:
                    axs[i,i2].view_init(elev=90, azim=-90)
                elif f==2:
                    axs[i,i2].view_init(elev=0, azim=-90)
                elif f==3:
                    axs[i,i2].view_init(elev=0, azim=0)
                i2 += 1
            i += 1
        plt.subplots_adjust(wspace=0, hspace=0.2)
        #label and tick a
        fig.text(0.02, 0.5, 'lenght', va='center', rotation='vertical')
        for i in range(len(a)):
            fig.text(0.04, 0.8-0.15*i, a[i], va='center')
        #label and tick b
        fig.text(0.5, 0.02, 'lenght2', va='center')
        for i in range(len(b)):
            fig.text(0.8-0.15*i, 0.04, b[i], va='center')

        plt.suptitle('4 points')
        plt.show()

def analysis():
    global result
    print("indices\n", result.describe(), sep="")
    print("correlation\n", result.corr(), sep="")
    #creating one long road merging all tests
    nodes = []
    prev_point = [0,0]
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, lenght3, angle3, res, radius1, radius2 = row
        xo, yo, x, y, x2, y2, x3, y3 = to4points(prev_point[0], prev_point[1], lenght1, angle1, lenght2, angle2, lenght3, angle3)
        nodes.append([x,y])
        nodes.append([x2,y2])
        nodes.append([x3,y3])
        prev_point = [x3,y3]
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

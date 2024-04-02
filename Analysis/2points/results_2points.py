import pandas as pd

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from test_analysis import *
from settings_utility import *

file_csv = "results_2points.csv"
result = None

def visualize():
    global result
    fig, ax = plt.subplots()
    i = -1
    j = -1
    lenght1_old = ""
    for row in result.itertuples(index=False):
        lenght1, angle1, res = row
        if lenght1 != lenght1_old:
            lenght1_old = lenght1
            i += 1
            j = -1
        j += 1
        if res == 1:
            ax.scatter(j, i, color="green")
        elif res == 2:
            ax.scatter(j, i, color="blue")
        # else:
        #     ax.scatter(j, i, color="red")
    x = result["angle1"].unique()
    y = result["lenght1"].unique()
    ax.set_xticks(range(len(x)))
    ax.set_xticklabels(x)
    ax.set_yticks(range(len(y)))
    ax.set_yticklabels(y)
    ax.set_xlabel('angle')
    ax.set_ylabel('lenght')
    ax.set_title('2 points')
    plt.show()

def analysis():
    global result
    print("indices\n", result.describe(), sep="")
    print("correlation\n", result.corr(), sep="")
    #creating one long road merging all tests
    nodes = []
    prev_point = [0,0]
    for row in result.itertuples(index=False):
        lenght1, angle1, res = row
        xo, yo, x, y = to2points(prev_point[0], prev_point[1], lenght1, angle1)
        nodes.append([x,y])
        prev_point = [x,y]
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

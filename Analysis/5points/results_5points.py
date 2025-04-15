import pandas as pd
import matplotlib.pyplot as plt

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from test_analysis import *
from settings_utility import *

file_csv = "results_5points.csv"
result = None

def analysis():
    global result
    print("indices\n", result.describe(), sep="")
    print("correlation\n", result.corr(), sep="")
    #creating one long road merging all tests
    nodes = []
    prev_point = [0,0]
    for row in result.itertuples(index=False):
        lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4, res, radius1, radius2, radius3 = row
        xo, yo, x, y, x2, y2, x3, y3, x4, y4 = to5points(prev_point[0], prev_point[1], lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4)
        nodes.append([x,y])
        nodes.append([x2,y2])
        nodes.append([x3,y3])
        nodes.append([x4,y4])
        prev_point = [x4,y4]
    _, dir_coverage = direction_coverage(nodes, 36, True)
    print("direction coverage\n", round(dir_coverage*100, 3), "%", sep="")

def main():
    global file_csv
    global result
    result = pd.read_csv(file_csv)
    analysis()

if __name__ == '__main__':
    main()

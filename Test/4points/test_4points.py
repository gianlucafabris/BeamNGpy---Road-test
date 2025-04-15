from beamngpy import BeamNGpy, Scenario, Vehicle, Road, MeshRoad
from scipy.spatial.transform import Rotation
import csv

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from settings_utility import *

file_csv = "results_4points.csv"

def main():
    global file_csv
    beamng = BeamNGpy('localhost', 64256, home=bngHome, user=bngUser)
    beamng.open(launch=True)

    print("in each senario will be displayed a grid of roads, showing all the combinations of rotation and lenght for the 2 segment of road as follows (. =  where are you)")
    for i in range(len(lenghts_lr)-1,-1,-1):
        print(lenghts_lr[i])
    print(".      ", end=" ")
    for t in angles2_lr:
        print(f"{t}º", end=" ")
    print(" ")
    print("each senario will differ form the previous one for the lenght of the 1 segment of road (rotation not needed) and lenght and rotation of the 2 segment of road")
    print("at the end of each senario, you will be prompted to input the result, 0 error 1 ok or 2 ok but intersects itself, follow this example - 10.0: 110101201110101022")
    data = []
    row = []
    row.append("lenght1")
    row.append("angle1")
    row.append("lenght2")
    row.append("angle2")
    row.append("lenght3")
    row.append("angle3")
    row.append("result")
    data.append(row)

    #i, dof rotation of 1 segment of road - 1 and 2 point, not necessary
    for j in range(len(lenghts_lr)): #dof lenght of 1 segment of road - 1 and 2 point

        for i2 in range(len(angles_lr)): #dof rotation of 2 segment of road - 2 and 3 point
            for j2 in range(len(lenghts_lr)): #dof lenght of 2 segment of road - 2 and 3 point
                print(f"senario - lenght1: {lenghts_lr[j]}, angles2: {angles_lr[i2]}, lenght2: {lenghts_lr[j2]}")
                scenario = Scenario('smallgrid', 'road_test')
                vehicle = Vehicle('ego_vehicle', model='etk800')
                scenario.add_vehicle(vehicle, pos=(0, 0, 0), rot_quat=Rotation.from_euler('xyz', [0, 0, np.radians(-135)]).as_quat())

                for i3 in range(len(angles2_lr)): #dof rotation of 3 segment of road - 3 and 4 point
                    xstart = 0
                    ystart = []
                    for j3 in range(len(lenghts_lr)): #dof lenght of 3 segment of road - 3 and 4 point
                        spacing = lenghts_lr[j3]+lenghts_lr[j2]+lenghts_lr[j]+10
                        xstart = i3*spacing
                        if j3 == 0:
                            ystart.append(0)
                        else:
                            ystart.append(ystart[j3-1]+spacing)
                        xo, yo, x, y, x2, y2, x3, y3 = to4points(xstart, ystart[len(ystart)-1], lenghts_lr[j], 0, lenghts_lr[j2], angles_lr[i2], lenghts_lr[j3], angles2_lr[i3])
                        #creating road
                        road = Road('track_editor_C_center')
                        road.add_nodes(tuple([round(el, 3) for el in np.array([xo, yo, 0.0])])) #1 point
                        road.add_nodes(tuple([round(el, 3) for el in np.array([x, y, 0.0])])) #2 point
                        road.add_nodes(tuple([round(el, 3) for el in np.array([x2, y2, 0.0])])) #3 point
                        road.add_nodes(tuple([round(el, 3) for el in np.array([x3, y3, 0.0])])) #4 point
                        scenario.add_road(road)

                scenario.make(beamng)
                try:
                    beamng.scenario.load(scenario)
                    beamng.scenario.start()
                    for j3 in range(len(lenghts_lr)):
                        values = input(f"{lenghts_lr[j3]}: ")
                        while len(values) != len(angles2_lr):
                            print("not all the required input were inserted, retry")
                            values = input(f"{lenghts_lr[j3]}: ")
                        for i3 in range(len(values)):
                            row = []
                            row.append(lenghts_lr[j])
                            row.append(0)
                            row.append(lenghts_lr[j2])
                            row.append(angles_lr[i2])
                            row.append(lenghts_lr[j3])
                            row.append(angles2_lr[i3])
                            row.append(int(values[i3]))
                            data.append(row)
                finally:
                    pass
    input("press enter to save the results in a csv")
    with open(file_csv, 'w', newline='') as file_csv:
        writer = csv.writer(file_csv)
        writer.writerows(data)
    beamng.close()

if __name__ == '__main__':
    main()

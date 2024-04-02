from beamngpy import BeamNGpy, Scenario, Vehicle, Road, MeshRoad
from scipy.spatial.transform import Rotation
import csv

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from settings_utility import *

file_csv = "results_2points.csv"

def main():
    global file_csv
    beamng = BeamNGpy('localhost', 64256, home=bngHome, user=bngUser)
    beamng.open(launch=True)

    print("in this senario will be displayed a grid of roads, showing all the combinations of rotation and lenght for the 2 segment of road as follows (. =  where are you)")
    for i in range(len(lenghts)-1,-1,-1):
        print(lenghts[i])
    print(".      ", end=" ")
    for t in angles:
        print(f"{t}º", end=" ")
    print(" ")
    print("at the end, you will be prompted to input the result, 0 error 1 ok or 2 ok but intersects itself, follow this example - 10.0: 110101201110101022")
    data = []
    row = []
    row.append("lenght1")
    row.append("angle1")
    row.append("result")
    data.append(row)

    scenario = Scenario('smallgrid', 'road_test')
    vehicle = Vehicle('ego_vehicle', model='etk800')
    scenario.add_vehicle(vehicle, pos=(0, 0, 0), rot_quat=Rotation.from_euler('xyz', [0, 0, np.radians(-135)]).as_quat())

    for i in range(len(angles)): #dof rotation of 1 segment of road - 1 and 2 point
        xstart = 0
        ystart = []
        for j in range(len(lenghts)): #dof lenght of 1 segment of road - 1 and 2 point
            spacing = lenghts[j]+10
            xstart = i*spacing
            if j == 0:
                ystart.append(0)
            else:
                ystart.append(ystart[j-1]+spacing)
            xo, yo, x, y = to2points(xstart, ystart[len(ystart)-1], lenghts[j], angles[i])
            #creating road
            road = Road('track_editor_C_center')
            road.add_nodes(tuple([round(el, 3) for el in np.array([xo, yo, 0.0])])) #1 point
            road.add_nodes(tuple([round(el, 3) for el in np.array([x, y, 0.0])])) #2 point
            scenario.add_road(road)

    scenario.make(beamng)
    try:
        beamng.scenario.load(scenario)
        beamng.scenario.start()
        for i in range(len(lenghts)):
            values = input(f"{lenghts[i]}: ")
            while len(values) != len(angles):
                print("not all the required input were inserted, retry")
                values = input(f"{lenghts[i]}: ")
            for j in range(len(values)):
                row = []
                row.append(lenghts[i])
                row.append(angles[j])
                row.append(int(values[j]))
                data.append(row)
    finally:
        input("press enter to save the results in a csv")
        with open(file_csv, 'w', newline='') as file_csv:
            writer = csv.writer(file_csv)
            writer.writerows(data)
        beamng.close()

if __name__ == '__main__':
    main()

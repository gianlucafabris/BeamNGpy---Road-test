from beamngpy import BeamNGpy, Scenario, Vehicle, Road, MeshRoad
from scipy.spatial.transform import Rotation
import csv

import os
import sys
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)
from settings_utility import *

file_csv = "results_5points.csv"

def main():
    global file_csv
    beamng = BeamNGpy('localhost', 64256, home=bngHome, user=bngUser)
    beamng.open(launch=True)

    print("in each senario will be displayed a grid of roads, showing all the combinations of rotation and lenght for the 2 segment of road as follows (. =  where are you)")
    for i in range(len(lenghts_llr)-1,-1,-1):
        print(lenghts_llr[i])
    print(".      ", end=" ")
    for t in angles2_llr:
        print(f"{t}º", end=" ")
    print(" ")
    print("each senario will differ form the previous one for the lenght of the 1 segment of road (rotation not needed), lenght and rotation of the 2 segment of road and lenght and rotation of the 3 segment of road")
    print("at the end of each senario, you will be prompted to input the result, 0 error 1 ok or 2 ok but intersects itself, follow this example - 10.0: 110101201110101022")
    data = []
    row = []
    row.append("lenght1")
    row.append("angle1")
    row.append("lenght2")
    row.append("angle2")
    row.append("lenght3")
    row.append("angle3")
    row.append("lenght4")
    row.append("angle4")
    row.append("result")
    data.append(row)

    #i, dof rotation of 1 segment of road - 1 and 2 point, not necessary
    for j in range(len(lenghts_llr)): #dof lenght of 1 segment of road - 1 and 2 point

        for i2 in range(len(angles_llr)): #dof rotation of 2 segment of road - 2 and 3 point
            for j2 in range(len(lenghts_llr)): #dof lenght of 2 segment of road - 2 and 3 point

                for i3 in range(len(angles2_llr)): #dof rotation of 3 segment of road - 3 and 4 point
                    for j3 in range(len(lenghts_llr)): #dof lenght of 3 segment of road - 3 and 4 point
                        print(f"senario - lenght1: {lenghts_llr[j]}, angles2: {angles_llr[i2]}, lenght2: {lenghts_llr[j2]}, angles3: {angles2_llr[i3]}, lenght3: {lenghts_llr[j3]}")
                        scenario = Scenario('smallgrid', 'road_test')
                        vehicle = Vehicle('ego_vehicle', model='etk800')
                        scenario.add_vehicle(vehicle, pos=(0, 0, 0), rot_quat=Rotation.from_euler('xyz', [0, 0, np.radians(-135)]).as_quat())

                        for i4 in range(len(angles2_llr)): #dof rotation of 4 segment of road - 4 and 5 point
                            xstart = 0
                            ystart = []
                            for j4 in range(len(lenghts_llr)): #dof lenght of 4 segment of road - 4 and 5 point
                                spacing = lenghts_llr[j4]+lenghts_llr[j3]+lenghts_llr[j2]+lenghts_llr[j]+10
                                xstart = i4*spacing
                                if j4 == 0:
                                    ystart.append(0)
                                else:
                                    ystart.append(ystart[j4-1]+spacing)
                                xo, yo, x, y, x2, y2, x3, y3, x4, y4 = to5points(xstart, ystart[len(ystart)-1], lenghts_llr[j], 0, lenghts_llr[j2], angles_llr[i2], lenghts_llr[j3], angles2_llr[i3], lenghts_llr[j4], angles2_llr[i4])
                                #creating road
                                road = Road('track_editor_C_center')
                                road.add_nodes(tuple([round(el, 3) for el in np.array([xo, yo, 0.0])])) #1 point
                                road.add_nodes(tuple([round(el, 3) for el in np.array([x, y, 0.0])])) #2 point
                                road.add_nodes(tuple([round(el, 3) for el in np.array([x2, y2, 0.0])])) #3 point
                                road.add_nodes(tuple([round(el, 3) for el in np.array([x3, y3, 0.0])])) #4 point
                                road.add_nodes(tuple([round(el, 3) for el in np.array([x4, y4, 0.0])])) #5 point
                                scenario.add_road(road)

                        scenario.make(beamng)
                        try:
                            beamng.scenario.load(scenario)
                            beamng.scenario.start()
                            for j4 in range(len(lenghts_llr)):
                                values = input(f"{lenghts_llr[j4]}: ")
                                while len(values) != len(angles2_llr):
                                    print("not all the required input were inserted, retry")
                                    values = input(f"{lenghts_llr[j4]}: ")
                                for i4 in range(len(values)):
                                    row = []
                                    row.append(lenghts_llr[j])
                                    row.append(0)
                                    row.append(lenghts_llr[j2])
                                    row.append(angles_llr[i2])
                                    row.append(lenghts_llr[j3])
                                    row.append(angles2_llr[i3])
                                    row.append(lenghts_llr[j4])
                                    row.append(angles2_llr[i4])
                                    row.append(int(values[i4]))
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

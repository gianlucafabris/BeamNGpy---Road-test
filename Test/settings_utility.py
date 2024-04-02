import numpy as np
import math

bngHome = "D:/Program Files (x86)/Steam/steamapps/common/BeamNG.drive"
bngUser = "C:/Users/gianluca/AppData/Local/BeamNG.drive"

def applyTraslation(point, traslation):
    return point+traslation

def applyRotation(point, traslation, theta):
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta),  np.cos(theta)]])
    tras = applyTraslation(point, traslation)
    rot = np.dot(rotation_matrix, tras)
    return applyTraslation(rot, traslation*-1)

def applyRotationArray(pointArray, theta):
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                [np.sin(theta),  np.cos(theta)]])
    return np.dot(rotation_matrix, pointArray)

def cartesian_to_polar(x, y):
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    return r, theta

def polar_to_cartesian(r, theta):
    x = r * math.cos(theta)
    y = r * math.sin(theta)
    return x, y

def to2points(xstart, ystart, lenght1, angle1):
    x, y = applyTraslation(np.array([xstart,ystart]), np.array(polar_to_cartesian(lenght1, math.radians(angle1))))
    return xstart, ystart, x, y

def to3points(xstart, ystart, lenght1, angle1, lenght2, angle2):
    _, _, x, y = to2points(xstart, ystart, lenght1, angle1)
    x2, y2 = applyTraslation(np.array([x,y]), applyRotation(np.array(polar_to_cartesian(lenght2, math.radians(angle2))), np.array([0, 0]), math.radians(angle1)))
    return xstart, ystart, x, y, x2, y2

def to4points(xstart, ystart, lenght1, angle1, lenght2, angle2, lenght3, angle3):
    _, _, x, y, x2, y2 = to3points(xstart, ystart, lenght1, angle1, lenght2, angle2)
    x3, y3 = applyTraslation(np.array([x2,y2]), applyRotation(applyRotation(np.array(polar_to_cartesian(lenght3, math.radians(angle3))), np.array([0, 0]), math.radians(angle1)), np.array([0, 0]), math.radians(angle2)))
    return xstart, ystart, x, y, x2, y2, x3, y3

def to5points(xstart, ystart, lenght1, angle1, lenght2, angle2, lenght3, angle3, lenght4, angle4):
    _, _, x, y, x2, y2, x3, y3 = to4points(xstart, ystart, lenght1, angle1, lenght2, angle2, lenght3, angle3)
    x4, y4 = applyTraslation(np.array([x3,y3]), applyRotation(applyRotation(applyRotation(np.array(polar_to_cartesian(lenght4, math.radians(angle4))), np.array([0, 0]), math.radians(angle1)), np.array([0, 0]), math.radians(angle2)), np.array([0, 0]), math.radians(angle3)))
    return xstart, ystart, x, y, x2, y2, x3, y3, x4, y4

#for 2 and 3 points will be used a higher resolution
nmin = 1
nmax = 250
iters = 10
base = math.e**((math.log(nmax)-math.log(nmin))/(iters-1))

angles = [j for j in range(0, 180, 10)]
angles2 = [j for j in range(-170, 180, 10)] #not used
lenghts = [round(base**i * nmin, 3) for i in range(iters)]

#for 4 points will be used a lower resolution
nmin_lr = 25
nmax_lr = 250
iters_lr = 5
base_lr = math.e**((math.log(nmax_lr)-math.log(nmin_lr))/(iters_lr-1))

angles_lr = [j for j in range(45, 180, 45)] #no 0 for correctness of the previous one
angles2_lr = [j for j in range(-135, 180, 45)]
lenghts_lr = [round(base_lr**i * nmin_lr, 3) for i in range(iters_lr)]

#for 5 points will be used a lower resolution
nmin_llr = 25
nmax_llr = 80
iters_llr = 3
base_llr = math.e**((math.log(nmax_llr)-math.log(nmin_llr))/(iters_llr-1))

angles_llr = [j for j in range(45, 180, 90)] #no 0 for correctness of the previous one
angles2_llr = [j for j in range(-135, 180, 90)]
lenghts_llr = [round(base_llr**i * nmin_llr, 3) for i in range(iters_llr)]

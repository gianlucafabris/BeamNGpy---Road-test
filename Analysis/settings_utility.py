import numpy as np
import math
import matplotlib.pyplot as plt

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

def visualizeCatmullrom(p_x, p_y):
    res = 100
    x_intpol, y_intpol = catmull_rom(p_x, p_y, res)
    p = np.concatenate((p_x, p_y))
    pmin = min(p) - 5
    pmax = max(p) + 5
    plt.figure(figsize=(10, 10))
    plt.plot(x_intpol, y_intpol)
    plt.scatter(p_x, p_y, color='black')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.xlim([pmin, pmax])
    plt.ylim([pmin, pmax])
    plt.grid(True)
    plt.show()

#part of the code is form https://github.com/vmichals/python-algos/blob/master/catmull_rom_spline.py\
def catmull_rom_coefficients(v0, v1, v2, v3):
    alpha = 0.5
    c1 = 0*alpha*v0 + 2*alpha*v1 + 0*alpha*v2 + 0*alpha*v3
    c2 = -1*alpha*v0 + 0*alpha*v1 + 1*alpha*v2 + 0*alpha*v3
    c3 = 2*alpha*v0 + -5*alpha*v1 + 4*alpha*v2 + -1*alpha*v3
    c4 = -1*alpha*v0 + 3*alpha*v1 + -3*alpha*v2 + 1*alpha*v3
    return (c1, c2, c3, c4)

def catmull_rom_one_point(x, v0, v1, v2, v3, d=0):
    """
    Computes interpolated y-coord for given x-coord using Catmull-Rom.
    Computes an interpolated y-coordinate for the given x-coordinate between
    the support points v1 and v2. The neighboring support points v0 and v3 are
    used by Catmull-Rom to ensure a smooth transition between the spline
    segments.
    Args:
        x: the x-coord, for which the y-coord is needed
        v0: 1st support point
        v1: 2nd support point
        v2: 3rd support point
        v3: 4th support point
        d: derivative
    Returns:
        y: value of y (given x) in that derivative
    """
    c1, c2, c3, c4 = catmull_rom_coefficients(v0, v1, v2, v3)
    if d == 0:
        return c1 + c2*x + c3*(x**2) + c4*(x**3)
    elif d == 1:
        return c2 + 2*c3*x + 3*c4*(x**2)
    elif d == 2:
        return 2*c3 + 6*c4*x
    elif d == 3:
        return 12*c4
    else:
        return 0

def catmull_rom(p_x, p_y, res=100, x=None, d=0):
    """
    Computes Catmull-Rom Spline for given support points and resolution.
    Args:
        p_x: array of x-coords
        p_y: array of y-coords
        res: resolution of a segment (including the start point, but not the endpoint of the segment) (only for d=0)
        x: point to derive (only for d>0)
        d: derivative
    Returns:
        (x,y): array for d=0 and single tuple for d>0, values of x,y in that derivative
    """
    if d == 0:
        x_intpol = np.empty(res*(len(p_x)-1) + 1)
        y_intpol = np.empty(res*(len(p_x)-1) + 1)
        x_intpol[-1] = p_x[-1]
        y_intpol[-1] = p_y[-1]
        # loop over segments (n-1 segments for n points)
        for i in range(len(p_x)-1):
            x_intpol[i*res:(i+1)*res] = np.linspace(p_x[i], p_x[i+1], res, endpoint=False)
            if i == 0:
                # need to estimate an additional support point before the first
                y_intpol[:res] = np.array([catmull_rom_one_point(x, p_y[0] - (p_y[1] - p_y[0]), p_y[0], p_y[1], p_y[2]) for x in np.linspace(0.,1.,res, endpoint=False)])
            elif i == len(p_x) - 2:
                # need to estimate an additional support point after the last
                y_intpol[i*res:-1] = np.array([catmull_rom_one_point(x, p_y[i-1], p_y[i], p_y[i+1], p_y[i+1] + (p_y[i+1] - p_y[i])) for x in np.linspace(0.,1.,res, endpoint=False)])
            else:
                y_intpol[i*res:(i+1)*res] = np.array([catmull_rom_one_point(x, p_y[i-1], p_y[i], p_y[i+1], p_y[i+2]) for x in np.linspace(0.,1.,res, endpoint=False)])
        return (x_intpol, y_intpol)
    else:
        i = np.searchsorted(p_x, x) - 1
        if i == 0:
            # need to estimate an additional support point before the first
            y = catmull_rom_one_point(x, p_y[0] - (p_y[1] - p_y[0]), p_y[0], p_y[1], p_y[2], d)
        elif i == len(p_x) - 2:
            # need to estimate an additional support point after the last
            y = catmull_rom_one_point(x, p_y[i-1], p_y[i], p_y[i+1], p_y[i+1] + (p_y[i+1] - p_y[i]), d)
        else:
            y = catmull_rom_one_point(x, p_y[i-1], p_y[i], p_y[i+1], p_y[i+2], d)
        return (x, y)

def radiusCurvature(p_x, p_y, x):
    first_derivative = catmull_rom(p_x, p_y, None, x, 1)
    second_derivative = catmull_rom(p_x, p_y, None, x, 2)
    if np.cross(first_derivative, second_derivative) != 0:
        r = abs(np.linalg.norm(first_derivative)**3/np.cross(first_derivative, second_derivative))
    else:
        # r = float("Inf")
        r = 0
    return r

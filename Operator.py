""" Basic vector operations. """

def add(a, b):
    return [a[0]+b[0], a[1]+b[1], a[2]+b[2]]

def sub(a, b):
    return [a[0]-b[0], a[1]-b[1], a[2]-b[2]]

def dot(a, b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

def cross(a, b):
    return [a[1]*b[2] - a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0]]

def neg(a):
    return [-a[0], -a[1], -a[2]]

def trace(a):
    return a[0][0] + a[1][1] + a[2][2]

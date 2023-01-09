from math import sqrt, acos, degrees

x1 = 0
y1 = 0
z1 = 1
x2 = -2.60011561e-02
y2 = 3.05472459e-02
z2 = -6.40000000e+01


def scalar(x1, y1, z1, x2, y2, z2):
    return (x1*x2 + y1*y2 + z1*z2)


def module(x, y, z):
    return sqrt(x**2 + y**2 + z ** 2)

cos = (scalar(x1, y1, z1, x2, y2, z2)) / (module(x1, y1, z1)*module(x2, y2, z2))

ang = acos(cos)

print(degrees(acos(cos)))

# import psycopg2
# # Connect to your postgres DB
# conn = psycopg2.connect("dbname=postgres user=postgres password=tamir662897")
#
# # Open a cursor to perform database operations
# cur = conn.cursor()
#
# # Execute a query
# cur.execute("SELECT * FROM test")
#
# # Retrieve query results
# records = cur.fetchall()
# print(records)


import matplotlib.pyplot
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

points = [[0.65612, 0.53440, 0.24175],
           [0.62279, 0.51946, 0.25744],
           [0.61216, 0.53959, 0.26394]]

p0, p1, p2 = points
x0, y0, z0 = p0
x1, y1, z1 = p1
x2, y2, z2 = p2

ux, uy, uz = u = [x1-x0, y1-y0, z1-z0]
vx, vy, vz = v = [x2-x0, y2-y0, z2-z0]

u_cross_v = [uyvz-uzvy, uzvx-uxvz, uxvy-uyvx]

point  = np.array(p0)
normal = np.array(u_cross_v)

d = -point.dot(normal)

xx, yy = np.meshgrid(range(10), range(10))

z = (-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]

# plot the surface
plt3d = plt.figure().gca(projection='3d')
plt3d.plot_surface(xx, yy, z)
plt.show()



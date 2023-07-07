from mesh_interface import *
from projection import *
import numpy as np


# Position is [X, Y, Z]
camera_position = [0, 0, 200]

# View is [r, Theta, Phi]
# Theta is the angle from the X axis and phi is the angle from the Z axis
camera_direction = [1, 0, np.pi]

"""
this angle SHOULD be looking directly down facing the x axis
"""
# two angles, showing the angle that we can see in either direction
field_of_view = [np.pi / 2, np.pi / 2]



triangles = read_stl("Cube.stl")
set_projection_coords(camera_position, camera_direction, triangles)
set_view_coords(field_of_view, triangles)

#print(triangles(triangles))

#print_relative_coords(triangles)

print_angle_coords(triangles)
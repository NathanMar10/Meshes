from mesh_interface import Vertex
import numpy as np
from camera_controller import Camera

"""
I literally 100% need to normalize the camera positions lol (but i think this happens after calculating things
so i dont really think that i care
"""


def set_projection_coords(camera: Camera, vertices: list[Vertex]):
    # I want to turn the camera normal into a camera projection matrix
    projection_matrix = create_projection_matrix(camera)



    camera_position_projected = get_projection(projection_matrix, camera.position)



    for vertex in vertices:

        # Sets relative coordinates in Viewspace coordinates

        vertex.relative_position = np.subtract(np.matmul(projection_matrix, vertex.position), camera_position_projected)

        # Finds the angles relative to the Viewspace axes

        squared_total = 0
        for coordinate in vertex.relative_position:
            squared_total += coordinate ** 2
        # Distance from the camera

        vertex.angle_position[0] = np.sqrt(squared_total)
        # Angle between N and U (Corresponds to horizontal angle)
        vertex.angle_position[1] = np.arctan(vertex.relative_position[0] / vertex.relative_position[2])
        # Angle between N and V (Corresponds to vertical angle)
        vertex.angle_position[2] = np.arctan(vertex.relative_position[1] / vertex.relative_position[2])



def create_projection_matrix(camera: Camera):

    u_array = np.array(camera.relative_axes[0])
    v_array = np.array(camera.relative_axes[1])
    n_array = np.array(camera.relative_axes[2])



    projection_matrix = np.column_stack((u_array, v_array, n_array))


    """
    print(u_array)
    print(v_array)
    print(n_array)
    print("Matrices: ")
    print(projection_matrix)
    print(transpose_matrix)
    """
    return np.transpose(projection_matrix)


def create_inverse_projection_matrix(camera: Camera):

    u_array = np.array(camera.relative_axes[0])
    v_array = np.array(camera.relative_axes[1])
    n_array = np.array(camera.relative_axes[2])



    projection_matrix = np.column_stack((u_array, v_array, n_array))


    """
    print(u_array)
    print(v_array)
    print(n_array)
    print("Matrices: ")
    print(projection_matrix)
    print(transpose_matrix)
    """
    return projection_matrix


def normalize(v: np.array):
    return v / np.linalg.norm(v)


def get_projection(matrix, vector: list):
    return np.matmul(matrix, np.array(vector))


# like 80% sure that this method works, but i just know that i 1) need the perpendicular distance parameterized and
# 2) need to have the angles relative to my view
def set_view_coords(camera: Camera, vertices: list[Vertex]):

    # Field of view can totally define me the values that will be valid




    # yer boy must find the perpendicular distance

    for vertex in vertices:

        # Calculate some projections for each of 'em
        # Should be the X coordinate on my display of the vertex?

        #print(triangle.angle_vertices[vertex_num])

        if np.abs(vertex.angle_position[1]) > camera.field_of_view[0] / 2 or np.abs(vertex.angle_position[2] > camera.field_of_view[1] / 2) or vertex.relative_position[2] < 0:
            # If any vertex is outside of my FOV im saying the whole triangle is. This won't stay, it should be once all are, but this is fine for now
            vertex.in_view = False
            break
        else:
            if (vertex.relative_position[2] == 0):
                print("You're Clipping into Something, hecker")
            vertex.displayed_position[0] = - camera.projection_distance / vertex.relative_position[2] * vertex.relative_position[0] + camera.screen_size[0] / 2
            # Should by the Y coordinate of the display
            #triangle.displayed_vertices[vertex_num][1] = distance_perpendicular * np.tan(triangle.angle_vertices[vertex_num][2])
            vertex.displayed_position[1] = camera.projection_distance / vertex.relative_position[2] * vertex.relative_position[1] + camera.screen_size[1] / 2
            # these values can (and literally should) be negative. To transform them into view space i wanna....
            # add width/2 to both
            # Distance from the Camera
            vertex.displayed_position[2] = vertex.angle_position[0]
            vertex.in_view = True


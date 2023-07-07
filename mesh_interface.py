import struct
import numpy as np

VERTEX_ROUNDING_LIMIT = .01


def read_stl(file_name):
    file = open(file_name, "rb")
    # Discard Header
    file.read(80)
    triangle_count = int.from_bytes(file.read(4), byteorder='little')
    print(triangle_count)
    triangles = []

    for x in range(triangle_count):
        triangles.append(Triangle(read_vector(file), [read_vector(file), read_vector(file), read_vector(file)]))
        file.read(2)  # Attribute Byte Count

    return triangles


def read_vector(file):
    x = struct.unpack('f', file.read(4))[0]
    y = struct.unpack('f', file.read(4))[0]
    z = struct.unpack('f', file.read(4))[0]
    return [np.round(x), np.round(y), np.round(z)]


def print_triangles(triangles: list):
    for x in range(len(triangles)):
        print("\nTriangle: " + str(x))
        print("N:  " + str(triangles[x].normal))
        for y in range(3):
            print("V1: " + str(triangles[x].vertices[y]))



def print_angle_coords(triangles: list):
    for x in range(len(triangles)):
        print("\nTriangle: " + str(x))
        print("N:  " + str(triangles[x].normal))
        for y in range(3):
            print("Actual V" + str(y + 1) + ": " + str(triangles[x].vertices[y]))
            print("Angle V" + str(y + 1) + ": " + str(triangles[x].angle_vertices[y]))
            print("Viewed V" + str(y + 1) + ": " + str(triangles[x].displayed_vertices[y]))

def print_relative_coords(triangles: list):
    for x in range(len(triangles)):
        print("\nTriangle: " + str(x) + "-----------------------------------")
        print("N:  " + str(triangles[x].normal))
        for y in range(3):
            print()
            print("Actual V" + str(y + 1) + ": " + str(triangles[x].vertices[y]))
            print("Relative V" + str(y + 1) + ": " + str(triangles[x].rel_vertices[y]))

def initialize_vertices(file_name):
    file = open(file_name, "rb")
    # Discard Header
    file.read(80)
    triangle_count = int.from_bytes(file.read(4), byteorder='little')
    vertices = set()

    for x in range(triangle_count):
        read_vector(file)
        for y in range(3):
            vertex_position = read_vector(file)
            vertices.add(Vertex(vertex_position))
        file.read(2)  # Attribute Byte Count


    print(len(vertices))

    vertex_dict = {}

    for vertex in vertices:
        vertex_dict[vertex.__hash__()] = vertex

    return vertex_dict



def get_x_coordinate(vertex):
    return vertex.position[0]

def initialize_triangles_to_vertices(file_name, vertex_dict):
    file = open(file_name, "rb")
    # Discard Header
    file.read(80)
    triangle_count = int.from_bytes(file.read(4), byteorder='little')
    print("Triangle Count: " + str(triangle_count))
    triangles = []

    for x in range(triangle_count):
        if x % 1000 == 0:
            print(x)
        normal = read_vector(file)

        vertex1_init = Vertex(read_vector(file))
        vertex2_init = Vertex(read_vector(file))
        vertex3_init = Vertex(read_vector(file))

        vertex1 = vertex_dict[vertex1_init.__hash__()]
        vertex2 = vertex_dict[vertex2_init.__hash__()]
        vertex3 = vertex_dict[vertex3_init.__hash__()]


        triangles.append(Triangle(normal, vertex1, vertex2, vertex3))

        file.read(2)  # Attribute Byte Count

    return triangles

def get_vertex(vertex_pos, vertices):

    vertices_set = set(vertices)
    this_vertex = Vertex(vertex_pos)

    index = vertices.index(this_vertex)
    return vertices[index]



def add_vertex(vertex, vertices):

    if vertex not in vertices:
        vertices.append(vertex)


def get_distance(pos1, pos2):
    return np.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2 + (pos1[2] - pos2[2]) ** 2)


class Vertex:
    def __init__(self, position: list[float]):
        self.position = position
        self.relative_position = [0, 0, 0]
        self.angle_position = [0, 0, 0]
        self.displayed_position = [0, 0, 0]

        self.in_view = False

    def __eq__ (self, other):
        if (self.position == other.position):
            return True;
        else:
            return False;

    def __hash__(self):
        return (int)(self.position[0] * 10000 + self.position[1] * 100 + self.position[2])




class Old_Triangle:

    def __init__(self, normal: list, vertices: list):
        self.normal = normal
        self.vertices = vertices

        self.rel_vertices = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.angle_vertices = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
        self.displayed_vertices = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]


        in_view = False

class Triangle:
    def __init__ (self, normal, vertex1, vertex2, vertex3):

        self.normal = normal
        self.vertices = [vertex1, vertex2, vertex3]
        in_view = False;

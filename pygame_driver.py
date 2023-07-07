import pygame
from mesh_interface import *
from projection import *
from camera_controller import *

import numpy as np


# My tris now just have a reference to the vertex list. I need to run every calc on all the vertices and then draw the lines using the tris
pygame.init()

screen_size = [1000, 1000]
root = pygame.display.set_mode(screen_size)
pygame.display.set_caption("Cringe Case")

# Camera Setup -------------------------------------------------------------------
# [X, Y, Z]
camera_position = [0 , -100, 0]

# [This is actually going to be the coordinates in which i am facing, but le normalized]
camera_direction = [ 0, 1, 0]

motion_increment = 10
rotation_increment = np.pi/16
FOV = 1

font = pygame.font.SysFont("Lucida Bright", 20)
position_header = font.render("Camera Position:", False, (255, 255, 255))
direction_header = font.render("Facing:", False, (255, 255, 255))
thetaphi_header = font.render("[Theta, Phi]:", False, (255, 255, 255))

camera = Camera(camera_position, camera_direction, screen_size, FOV)


stl_file = "3dbenchy.STL"
vertices = initialize_vertices(stl_file)
print("I want you to know that i finished when i did it")
#simplify_vertices(vertices)
triangles = initialize_triangles_to_vertices(stl_file, vertices)


#more_triangles = read_stl("Cube.stl")

print("ya done good")
vertices = list(vertices.values())

#triangles += more_triangles

set_projection_coords(camera, vertices)
set_view_coords(camera, vertices)

circle_img = pygame.image.load("Vertex_img.png")
circle_img = pygame.transform.scale(circle_img, (1, 1))
SCALE_FACTOR = 1

def draw_vertices():
    root.fill(color="Black")
    for triangle in triangles:

        in_view = True
        for vertex in triangle.vertices:
            if not vertex.in_view:
                in_view = True
        if not in_view:
            continue

        first_vertex = [triangle.vertices[0].displayed_position[0] * SCALE_FACTOR, triangle.vertices[0].displayed_position[1] * SCALE_FACTOR]
        second_vertex = [triangle.vertices[1].displayed_position[0] * SCALE_FACTOR, triangle.vertices[1].displayed_position[1] * SCALE_FACTOR]
        third_vertex = [triangle.vertices[2].displayed_position[0] * SCALE_FACTOR, triangle.vertices[2].displayed_position[1] * SCALE_FACTOR]

        pygame.draw.line(root, color="white", start_pos=first_vertex, end_pos=second_vertex)
        pygame.draw.line(root, color="white", start_pos=second_vertex, end_pos=third_vertex)
        pygame.draw.line(root, color="white", start_pos=third_vertex, end_pos=first_vertex)

    root.blit(position_header, dest = (screen_size[0] - 400, 0))
    root.blit(direction_header, dest=(screen_size[0] - 400, 20))
    root.blit(thetaphi_header, dest=(screen_size[0] - 400, 40))
    root.blit(font.render(str(camera.get_position_rounded()), False, (255, 255, 255)), dest= (screen_size[0] - 200, 0))
    root.blit(font.render(str(camera.get_heading_rounded()), False, (255, 255, 255)), dest=(screen_size[0] - 200, 20))
    root.blit(font.render(str(get_theta_phi(camera.relative_axes[2])), False, (255, 255, 255)), dest=(screen_size[0] - 200, 40))



draw_vertices()

exit = False

while not exit:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
           exit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                camera.move_up()
            if event.key == pygame.K_a:
                camera.move_left()
            if event.key == pygame.K_s:
                camera.move_down()
            if event.key == pygame.K_d:
                camera.move_right()
            if event.key == pygame.K_SPACE:
                camera.move_forward()
            if event.key == pygame.K_LSHIFT:
                camera.move_backward()

            if event.key == pygame.K_i:
                camera.rotate_up()
            if event.key == pygame.K_j:
                camera.rotate_left()
            if event.key == pygame.K_k:
                camera.rotate_down()
            if event.key == pygame.K_l:
                camera.rotate_right()


            set_projection_coords(camera, vertices)
            set_view_coords(camera, vertices)
            draw_vertices()
        pygame.display.update()



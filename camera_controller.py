import numpy as np
import projection

DEFAULT_MOVE_INCREMENT = 25
# Units are turns/ click
DEFAULT_ROTATION_INCREMENT = 1/32* np.pi



###### MAKE THE CAMERA DIRECTION STORED IN A UNIT VECTOR ALONG WITH THE ANGLE VECTOR
###### Its used as an angle to make the other vectors, but if i can make V without the angle stuff i can totally get
### rid of it (although i can totally make it just create the angles in createprojectionmatric


class Camera:

    def __init__(self, position, direction, screen_size, FOV):

        # Position is relative to the World Coordinates
        self.position = position
        # Direction is [X, Y, Z] also , showing where the camera is pointing
        self.relative_axes = get_relative_axes(projection.normalize(direction))

        # Screen size to be displayed
        self.screen_size = screen_size
        # [Horizontal, Vertical] as total angles
        self.field_of_view = (np.pi/1.5, np.pi/1.5)
        self.projection_distance = 1000

        self.move_increment = DEFAULT_MOVE_INCREMENT
        self.rotation_increment = DEFAULT_ROTATION_INCREMENT

    def set_move_increment(self, move_increment: float):
        self.move_increment = move_increment

    def set_rotation_increment(self, rotation_increment: float):
        self.rotation_increment = rotation_increment



    def move_right(self):
        for x in range(3):
            self.position[x] += self.move_increment * self.relative_axes[0][x]
    def move_left(self):
        for x in range(3):
            self.position[x] -= self.move_increment * self.relative_axes[0][x]
    def move_up(self):
        for x in range(3):
            self.position[x] += self.move_increment * self.relative_axes[1][x]
    def move_down(self):
        for x in range(3):
            self.position[x] -= self.move_increment * self.relative_axes[1][x]
    def move_forward(self):
        for x in range(3):
            self.position[x] += self.move_increment * self.relative_axes[2][x]
    def move_backward(self):
        for x in range(3):
            self.position[x] -= self.move_increment * self.relative_axes[2][x]


    def rotate_up(self):
        # Args given in [U, V, N]
        self.set_new_direction((0, np.sin(self.rotation_increment), np.cos(self.rotation_increment)))


    def rotate_down(self):
        # Args given in [U, V, N]
        self.set_new_direction((0, np.sin(-self.rotation_increment), np.cos(-self.rotation_increment)))

    def rotate_left(self):
        # Args given in [U, V, N]
        self.set_new_direction((np.sin(self.rotation_increment), 0, np.cos(self.rotation_increment)))

    def rotate_right(self):
        # Args given in [U, V, N]
        self.set_new_direction((np.sin(-self.rotation_increment), 0, np.cos(-self.rotation_increment)))


    def get_position_rounded(self):
        x = np.round(self.position[0])
        y = np.round(self.position[1])
        z = np.round(self.position[2])
        return (x, y, z)




    def get_heading_rounded(self):
        vector = [0, 0, 0]
        for x in range(3):
            vector[x] = np.round(self.relative_axes[2][x], decimals=2)
        return vector

    def set_new_direction(self, new_direction: list[float]):
        #Input arg is the new direction in UVN space, so i can unproject it to get the XYZ space

        # So we need to literally just set them i guess RIGHT???

        unproject_matrix = projection.create_inverse_projection_matrix(self)
        self.relative_axes = get_relative_axes(np.matmul(unproject_matrix, new_direction))









def get_relative_axes(n: list[float]):
    # Direction inputs my n vector and i need to get my v

    theta_phi = get_theta_phi(n)



    v = [np.sin(theta_phi[1] - np.pi / 2) * np.cos(theta_phi[0]),
        np.sin(theta_phi[1] - np.pi / 2) * np.sin(theta_phi[0]),
        np.cos(theta_phi[1] - np.pi / 2)]

    u = np.cross(v, n)

    return [u, v, n]

def get_theta_phi(n: list[float]):
    x_y_mag = np.sqrt(n[0] ** 2 + n[1] ** 2)

    if n[2] != 0:
        phi = np.arctan(x_y_mag / n[2])
        if phi < 0:
            phi += np.pi
    else:
        phi = np.pi / 2

    if n[0] != 0:
        #print(n[0], n[1])
        theta = np.arctan(n[1] / n[0])
        if n[0] < 0:
            theta += np.pi

    else:
        if n[1] > 0:
            theta = np.pi / 2
        else:
            theta = - np.pi / 2

    return [np.round(theta, decimals=2), np.round(phi, decimals=2)]




def get_field_of_view(screen_size, FOV):
    return [np.pi/2, np.pi/2]


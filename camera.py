import pygame
import math
import time
import matrix

from matrix import Mat4, getMatrixInverse
from functions import cap
from pygame import Vector3

HALF_PI = math.pi / 2

class Camera:
    def __init__(self, x=0, y=0, z=6):
        self.pos = Vector3(x, y, z)
        self.pitch: float = 0.0
        self.yaw: float = 0.0 
        self.roll: float = 0.0
        self.speed: int = 20
        self.forward = Vector3(0)

        self.start_time: float = 0.0
        self.dt: float = 0.0
        self.world_matrix = None

    @property
    def x(self):
        return self.pos[0]

    @property
    def y(self):
        return self.pos[1]

    @property
    def z(self):
        return self.pos[2]

    def move(self, vec) -> None:
        self.pos += vec

    def addPitch(self, amount) -> None:
        self.pitch += amount

    def addRoll(self, amount) -> None:
        self.roll += amount

    def addYaw(self, amount) -> None:
        self.yaw += amount

    def update(self):
        current_time = time.time()
        self.dt = current_time - self.start_time
        self.start_time = current_time

        keys = pygame.key.get_pressed()
        dx, dy = pygame.mouse.get_rel()

        self.forward = Vector3(0, 0, -1)
        self.forward.rotate_y_ip_rad(self.pitch)

        if keys[pygame.K_UP]:
            self.pos[1] += 0.05
        if keys[pygame.K_DOWN]:
            self.pos[1] -= 0.05
        if keys[pygame.K_w]:
            self.move(self.forward * self.speed * self.dt)
        if keys[pygame.K_s]:
            self.move(-self.forward * self.speed * self.dt)

        self.addRoll(-dy * 0.5 * self.dt)
        self.addPitch(dx * 0.5 * self.dt)

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            left = Vector3(-1, 0, 0)
            left.rotate_y_ip_rad(self.pitch)
            self.move(left * self.speed * self.dt)


        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            right = Vector3(1, 0, 0)
            right.rotate_y_ip_rad(self.pitch)
            self.move(right * self.speed * self.dt)

    def get_view_matrix(self):

        rotation_yaw = matrix.get_roll(self.roll)
        rotation_pitch = matrix.get_pitch(self.pitch)
        translation = matrix.get_translation_mat(*(-self.pos))

        self.world_matrix = rotation_yaw.mat4_dot(rotation_pitch).mat4_dot(translation)
        return getMatrixInverse(self.world_matrix)

        cos_pitch = math.cos(self.pitch)
        sin_pitch = math.sin(self.pitch)
        cos_yaw = math.cos(self.yaw)
        sin_yaw = math.sin(self.yaw)

        x_axis = Vector3([cos_yaw, 0, -sin_yaw])
        y_axis = Vector3([sin_yaw * sin_pitch, cos_pitch, cos_yaw * sin_pitch])
        z_axis = Vector3([sin_yaw * cos_pitch, -sin_pitch, cos_pitch * cos_yaw])

        eye = self.pos

        return Mat4(
            [
              [x_axis[0], y_axis[0], z_axis[0], 0],
              [x_axis[1], y_axis[1], z_axis[1], 0],
              [x_axis[2], y_axis[2], z_axis[2], 0],
              [x_axis.dot(eye) , y_axis.dot(eye), z_axis.dot(eye), 1]
            ]
          )

import constants
import polygon_clipper
import pygame
import pygame.gfxdraw


from pygame.time import Clock
from pygame.draw import polygon as draw_polygon
from matrix import Mat4
from pprint import pprint
from pygame import Vector3, Vector2
from models import CubeData


def z_sort(quad):
    q = quad[0]
    return sum([v[0].z for v in q]) / len(q)


VECTOR_CEN = Vector3(1, 1, 0)

class Pipeline:
    def __init__(self, world):
        self.world = world
        self.setup_projection_matrix()

        self.main_matrix = world.camera.get_view_matrix().mat4_dot(self.projection_matrix)
        self.scale_x, self.scale_y = self.world.engine.width / 2, self.world.engine.height / 2
        self.display = world.engine.display

        self.cache = {}
        self.sorted_polygons = []
        self.texture = pygame.image.load('floor.png')
        self.texture.convert()
        self.clock = Clock()

    def setup_projection_matrix(self):
        aspect_ratio = self.world.engine.height / self.world.engine.width
        far_near_difference = constants.FAR_PLANE - constants.NEAR_PLANE

        self.projection_matrix = Mat4(
            [
              [constants.FOV_COT * aspect_ratio, 0, 0, 0],
              [0, constants.FOV_COT, 0, 0],
              [0, 0, (constants.FAR_PLANE - constants.NEAR_PLANE) / far_near_difference, 1],
              [0, 0, -(2 * constants.FAR_PLANE * constants.NEAR_PLANE) / far_near_difference, 0]
            ]
                )

    def set_light(self, light_pos):
        self.light_pos = Vector3(light_pos)
        self.light_pos.normalize_ip()

    def send(self, mesh):
        main_dot = self.main_matrix.vec_dot
        s_append = self.sorted_polygons.append 
        p_clip = polygon_clipper.clip_polygon
        p_dot = self.cam_world.dot
        Normals = CubeData.NORMALS

        for quad, normal_index, pn in mesh:
            normal = Normals[normal_index]

            #  backface culling
            if p_dot(normal) < pn:
                continue

            #  main matrix multiplication
            quad = [main_dot(v) for v in quad]

            #  clipping
            clipped = p_clip(quad)
            if clipped:  # is empty?
                s_append((clipped, normal))

        self.sorted_polygons.sort(key=z_sort, reverse=True)
        self.rasterize_polygons(self.sorted_polygons)

    def rasterize_polygons(self, polygons):
        screen_polygon = []
        _append = screen_polygon.append
        _display = self.world.engine.display
        _sx = self.scale_x
        _sy = self.scale_y
        _light_dot = self.light_pos.dot
        for polygon, normal in polygons:
            screen_polygon.clear() 
            for vertex in polygon:
                w = vertex[1]
                if not w:  # not 0
                    w = 0.00001
                ndc_vec = ((vertex[0] / w) + VECTOR_CEN)  # normalize device coordinates
                screen_point = (ndc_vec.x) * _sx, (ndc_vec.y) * _sy
                _append(screen_point)
            
            #color calculation based on light value
            dp = _light_dot(normal)
            value = int(255 / abs(dp + 2.4))
            color = (value,) * 3

            draw_polygon(_display, color, screen_polygon, width=1)
            draw_polygon(_display, color, screen_polygon, width=0)

    def update(self):
        self.cache.clear()
        self.sorted_polygons.clear()

        self.view_matrix = self.world.camera.get_view_matrix()
        self.main_matrix = self.view_matrix.mat4_dot(self.projection_matrix)

        # self.point = self.world.camera.world_matrix.vec_dot(VECTOR_0)
        # world_matrix.dot(Vector0)
        self.cam_world = Vector3(self.world.camera.world_matrix.mat[3][:3])


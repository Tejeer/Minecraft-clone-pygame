import noise
import random

from graphics_pipeline import Pipeline
from random import randint
from models import Voxel
from renderer import Renderer
from camera import Camera
from chunk_sys import ChunkSys
from pprint import pprint


class World:

    def __init__(self, engine):
        self.engine = engine

        self.renderer = Renderer(self.engine)
        self.camera = Camera()
        self.chunks = ChunkSys()

        n = 30
        seed = 0.50#random.randint(0, 10000) / 10000
        cols = [0]
        for x in range(n):
            for y in range(5):
                for z in range(n):
                    val = int(abs(noise.snoise3(x / n, z / n, seed)) * 4) 
                    for p in range(val):
                        self.chunks.add_block([x, -p, z], Voxel())
                   #  if y in cols and randint(0, 1) == 1:
                        # self.chunks.add_block([x, y, z], Voxel())
                    # elif y > max(cols):
                    #     self.chunks.add_block([x, y, z], Voxel())

        self.mesh = []
        # for chunk_pos in self.chunks.chunks:
            # self.mesh += self.chunks.greedy_mesh(chunk_pos)

        self.chunks.update_mesh_buffer()

        self.pipeline = Pipeline(self)
        self.pipeline.set_light([110 , 129480123, 123988993])


    def update(self):
        self.update_objects()
        self.camera.update()

    def render(self):
        self.renderer.show_fps()

    def update_objects(self):
        self.mesh.clear()
        for mesh in self.chunks.mesh_buffer:
            self.mesh.extend(self.chunks.mesh_buffer[mesh])
        self.pipeline.update()
        self.pipeline.send(self.mesh)

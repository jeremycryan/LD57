import math
import random

import pygame

from image_manager import ImageManager
from primitives import Pose
import platform


class Particle:

    def __init__(self, position=(0, 0), velocity=(0, 0), duration=1.0):
        self.position = Pose(position)
        self.velocity = Pose(velocity)
        self.destroyed = False
        self.duration = duration
        self.age = 0
        self.layer = 1

    def get_scale(self):
        return 1

    def get_alpha(self):
        return 255

    def update(self, dt, events):
        if self.destroyed:
            return
        self.position += self.velocity * dt
        if self.age > self.duration:
            self.destroy()
        self.age += dt

    def draw(self, surf, offset=(0, 0)):
        if self.destroyed:
            return

    def through(self):
        return min(0.999, self.age/self.duration)

    def destroy(self):
        self.destroyed = True


class Dust(Particle):

    SURF = None

    def __init__(self, position=(0, 0), duration = 0.5, surface_for_reference = None, outline_points = None):

        self.surf = ImageManager.load("assets/images/dust.png")
        spawn_area_width = surface_for_reference.get_width()
        spawn_area_height = surface_for_reference.get_height()
        position_local = random.choice(outline_points) if outline_points else (0, 0)
        if (outline_points):
            position_local = position_local[0] - surface_for_reference.get_width()//2, position_local[1] - surface_for_reference.get_height()//2
        velocity = position_local[0] * 4 * random.random(), position_local[1] * 4 * random.random()
        position = position[0] + position_local[0], position[1] + position_local[1]
        super().__init__(position, velocity, duration)
        self.rotation = random.random() * 360
        self.scale_factor = max(0.2, min(1, (spawn_area_width + spawn_area_height)/2 / 200)) * (random.random() * 0.5 + 0.5)
        self.initial_velocity = self.velocity

    def get_scale(self):
        return (1 - self.through() **0.7) * self.scale_factor

    def get_alpha(self):
        return (1 - self.through())**2 * 128

    def update(self, dt, events):
        self.velocity = self.initial_velocity * (1 - self.through()) ** 2
        super().update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        scale = self.get_scale()
        surf = pygame.transform.scale(self.surf, (self.surf.get_width() * scale, self.surf.get_height() * scale))
        surf = pygame.transform.rotate(surf, self.rotation)
        surf.set_alpha(self.get_alpha())
        x = offset[0] + self.position.x - surf.get_width()//2
        y = offset[1] + self.position.y - surf.get_height()//2
        surface.blit(surf, (x, y))



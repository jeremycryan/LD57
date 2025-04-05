import time

import pygame

from grabbable import Grabbable, GeometricContainer
from grabbable_manager import GrabbableManager
from image_manager import ImageManager
from sound_manager import SoundManager
import constants as c


class Frame:
    def __init__(self, game):
        self.game = game
        self.done = False

    def load(self):
        pass

    def update(self, dt, events):
        pass

    def draw(self, surface, offset=(0, 0)):
        surface.fill((128, 128, 128))

    def next_frame(self):
        return Frame(self.game)

class PackingFrame(Frame):
    def load(self):
        self.grabbable_manager = GrabbableManager(self)
        self.grabbable_manager.add_grabbables(
            Grabbable(self, Grabbable.square_surface((160, 25, 40), 200, 100)),
            Grabbable(self, Grabbable.square_surface((170, 140, 0), 125, 125)),
            Grabbable(self, Grabbable.square_surface((30, 60, 160), 60, 60)),
            GeometricContainer(self, Grabbable.square_surface((255, 255, 255), 300, 175), position = (c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT//2)),
        )

    def update(self, dt, events):
        self.grabbable_manager.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        surface.fill((128, 128, 128))
        self.grabbable_manager.draw(surface, offset)

    def next_frame(self):
        return Frame(self.game)
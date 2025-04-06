import time

import pygame

from banner_toast import BannerToast
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
        LEVELS = [[
            Grabbable(self, ImageManager.load("assets/images/charger.png"), name="Charger",
                      position=(1152 / 2, 309 / 2)),
            Grabbable(self, ImageManager.load("assets/images/mouse.png"), name="Mouse", position=(968 / 2, 668 / 2)),
            Grabbable(self, ImageManager.load("assets/images/ban.png"), name="Laptop", position=(372 / 2, 609 / 2)),
            Grabbable(self, ImageManager.load("assets/images/headphones.png"), name="Headphones",
                      position=(242 / 2, 561 / 2)),
            Grabbable(self, ImageManager.load("assets/images/toothbrush.png"), name="Toothbrush",
                      position=(108 / 2, 167 / 2)),
            Grabbable(self, ImageManager.load("assets/images/toothpaste.png"), name="Toothpaste",
                      position=(1053 / 2, 297 / 2)),
            Grabbable(self, ImageManager.load("assets/images/soap.png"), name="Soap", position=(73 / 2, 216 / 2)),
            Grabbable(self, ImageManager.load("assets/images/pillow.png"), name="Pillow", position=(31 / 2, 405 / 2)),
            GeometricContainer(self,
                               ImageManager.load("assets/images/suitcase_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/suitcase_open.png"),
                               closed_surf=ImageManager.load("assets/images/suitcase_closed.png"),
                               position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 3),
                               is_suitcase=True, name="Suitcase"),
            GeometricContainer(self,
                               ImageManager.load("assets/images/toiletry_bag_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/toiletry_bag_open.png"),
                               closed_surf=ImageManager.load("assets/images/toiletry_bag_closed.png"),
                               name="Toiletry Bag",
                               position=(1116 / 2, 633 / 2)),
            GeometricContainer(self,
                               ImageManager.load("assets/images/laptop_bag_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/laptop_bag_open.png"),
                               closed_surf=ImageManager.load("assets/images/laptop_bag_closed.png"),
                               name="Laptop Bag",
                               position=(1190 / 2, 162 / 2)),
            # GeometricContainer(self,
            #                    ImageManager.load("assets/images/bag_of_holding_open_placeable_area.png"),
            #                    draw_surf=ImageManager.load("assets/images/bag_of_holding_open.png"),
            #                    closed_surf=ImageManager.load("assets/images/bag_of_holding_closed.png"),
            #                    position=(c.WINDOW_WIDTH * 0.9, c.WINDOW_HEIGHT * 0.9),
            #                    name="Bag of Holding"),
        ],
        [
            GeometricContainer(self,
                               ImageManager.load("assets/images/suitcase_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/suitcase_open.png"),
                               closed_surf=ImageManager.load("assets/images/suitcase_closed.png"),
                               position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 3),
                               is_suitcase=True, name="Suitcase"),
            GeometricContainer(self,
                               ImageManager.load("assets/images/backpack_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/backpack_open.png"),
                               closed_surf=ImageManager.load("assets/images/backpack_closed.png"),
                               position=(104, 65),
                               name="Backpack",
                               contents=[
                                   Grabbable(self, ImageManager.load("assets/images/catryoshka_4.png"),
                                             name="Catryoshka",
                                             position=(106, 42), can_only_contain=["Catryoshka"],
                                             contents_must_be_smaller=True),
                               ]),
            Grabbable(self, ImageManager.load("assets/images/crouton.png"), name="Crouton",
                      position=(59, 106), alive=True, can_only_be_placed_in=["Cat Carrier"]),
            GeometricContainer(self,
                               ImageManager.load("assets/images/cat_carrier_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/cat_carrier_open.png"),
                               closed_surf=ImageManager.load("assets/images/cat_carrier_closed.png"),
                               name="Cat Carrier",
                               position=(565, 95), contents = [
                    GeometricContainer(self,
                                       ImageManager.load("assets/images/moonsigil_scroll_open_placeable_area.png"),
                                       draw_surf=ImageManager.load("assets/images/moonsigil_scroll.png"),
                                       closed_surf=ImageManager.load("assets/images/moonsigil_scroll_closed.png"),
                                       name="Sigil Scroll",
                                       position=(564, 141),
                                       contents = [
                                           Grabbable(self, ImageManager.load("assets/images/catryoshka_6.png"),
                                                     name="Catryoshka",
                                                     position=(567, 136), can_only_contain=["Catryoshka"],
                                                     contents_must_be_smaller=True),
                                       ]),
                    Grabbable(self, ImageManager.load("assets/images/catryoshka_3.png"), name="Catryoshka",
                              position=(602, 98), can_only_contain=["Catryoshka"],
                              contents_must_be_smaller=True),
                ]),
            Grabbable(self, ImageManager.load("assets/images/sigil_1.png"), name="Sigil",
                      position=(69, 251), can_only_be_placed_in=["Sigil Scroll"]),
            Grabbable(self, ImageManager.load("assets/images/sigil_2.png"), name="Sigil",
                      position=(539, 221), can_only_be_placed_in=["Sigil Scroll"]),
            Grabbable(self, ImageManager.load("assets/images/catryoshka_1.png"), name="Catryoshka",
                      position=(513, 175), can_only_contain=["Catryoshka"], contents_must_be_smaller=True),
            Grabbable(self, ImageManager.load("assets/images/catryoshka_2.png"), name="Catryoshka",
                      position=(60, 209), can_only_contain=["Catryoshka"],
                      contents_must_be_smaller=True),
            Grabbable(self, ImageManager.load("assets/images/catryoshka_5.png"), name="Catryoshka",
                      position=(74, 221), can_only_contain=["Catryoshka"],
                      contents_must_be_smaller=True),
            Grabbable(self, ImageManager.load("assets/images/cat_food.png"), name="Cat Food",
                      position=(122, 231)),
            Grabbable(self, ImageManager.load("assets/images/scoop.png"), name="Scoop",
                      position=(530, 300)),
            Grabbable(self, ImageManager.load("assets/images/toy.png"), name="Cat Toy",
                      position=(542, 326)),

        ]
        ]
        LEVEL_EASY = [
        GeometricContainer(self,
                           ImageManager.load("assets/images/suitcase_open_placeable_area.png"),
                           draw_surf=ImageManager.load("assets/images/suitcase_open.png"),
                           closed_surf=ImageManager.load("assets/images/suitcase_closed.png"),
                           position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 3),
                           is_suitcase=True, name="Suitcase"),
        Grabbable(self, ImageManager.load("assets/images/toy.png"), name="Cat Toy",
                  position=(542, 326)),
        ]
        for item in LEVELS[self.game.current_level]:
            self.grabbable_manager.add_grabbable(item)

        self.banner_toast = BannerToast(self)
        self.banner_toast.show("Pack your suitcase!")

    def update(self, dt, events):
        self.grabbable_manager.update(dt, events)
        self.banner_toast.update(dt, events)
        if self.grabbable_manager.completed and self.banner_toast.faded_to_black and not self.done:
            self.done = True
            self.game.current_level += 1

    def draw(self, surface, offset=(0, 0)):
        surface.fill((128, 128, 128))
        self.grabbable_manager.draw(surface, offset)
        self.banner_toast.draw(surface, offset)

    def next_frame(self):
        return PackingFrame(self.game)
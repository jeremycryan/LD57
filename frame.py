import time

import pygame

from banner_toast import BannerToast
from grabbable import Grabbable, GeometricContainer
from grabbable_manager import GrabbableManager
from image_manager import ImageManager
from sound_manager import SoundManager
import constants as c
from Button import Button
import platform

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

    def name(self):
        return self.__class__.__name__



class PackingFrame(Frame):
    def load(self):
        self.grabbable_manager = GrabbableManager(self)
        LEVELS = [[
            Grabbable(self, ImageManager.load("assets/images/charger.png"), name="Charger",
                      position=(1152 / 2, 309 / 2), shadow_height=4),
            Grabbable(self, ImageManager.load("assets/images/mouse.png"), name="Mouse", position=(968 / 2, 668 / 2)),
            Grabbable(self, ImageManager.load("assets/images/ban.png"), name="Laptop", position=(372 / 2, 609 / 2)),
            Grabbable(self, ImageManager.load("assets/images/headphones.png"), name="Headphones",
                      position=(242 / 2, 561 / 2)),
            Grabbable(self, ImageManager.load("assets/images/toothbrush.png"), name="Toothbrush",
                      position=(108 / 2, 167 / 2), shadow_height=2),
            Grabbable(self, ImageManager.load("assets/images/toothpaste.png"), name="Toothpaste",
                      position=(1053 / 2, 297 / 2), shadow_height=3),
            Grabbable(self, ImageManager.load("assets/images/soap.png"), name="Soap", position=(73 / 2, 216 / 2), shadow_height=3),
            Grabbable(self, ImageManager.load("assets/images/pillow.png"), name="Pillow", position=(31 / 2, 405 / 2)),
            GeometricContainer(self,
                               ImageManager.load("assets/images/suitcase_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/suitcase_open.png"),
                               closed_surf=ImageManager.load("assets/images/suitcase_closed.png"),
                               position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT * 0.3),
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
        ],
        [
            GeometricContainer(self,
                               ImageManager.load("assets/images/suitcase_open_placeable_area.png"),
                               draw_surf=ImageManager.load("assets/images/suitcase_open.png"),
                               closed_surf=ImageManager.load("assets/images/suitcase_closed.png"),
                               position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT * 0.3),
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

        ],
            [
                GeometricContainer(self,
                                   ImageManager.load("assets/images/suitcase_open_placeable_area.png"),
                                   draw_surf=ImageManager.load("assets/images/suitcase_open.png"),
                                   closed_surf=ImageManager.load("assets/images/suitcase_closed.png"),
                                   position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT * 0.3),
                                   is_suitcase=True, name="Suitcase"),
                Grabbable(self, ImageManager.load("assets/images/egg.png"),
                          name="Egg of the Eternal Void",
                          position=(23, 115),
                          cannot_be_placed_in_anything=True,
                          can_contain_things=True,
                          can_only_contain="Suitcase",
                          capacity=1),
                Grabbable(self, ImageManager.load("assets/images/nes.png"),
                          name="Nantucket Entertainment System",
                          position=(60, 165), can_only_contain_tags=["Game Cartridge"]),
                Grabbable(self, ImageManager.load("assets/images/charizard.png"),
                          name="Chardragon",
                          position=(513, 68),
                          tags=["Game Card"], shadow_height=2),
                GeometricContainer(self,
                                   ImageManager.load("assets/images/kentucky_open_placeable_area.png"),
                                   draw_surf=ImageManager.load("assets/images/kentucky_open.png"),
                                   closed_surf=ImageManager.load("assets/images/kentucky_closed.png"),
                                   position=(575, 31),
                                   name="Kentucky Box",
                                   contents = [
                                       GeometricContainer(self,
                                                          ImageManager.load(
                                                              "assets/images/scrumble_open_placeable_area.png"),
                                                          draw_surf=ImageManager.load(
                                                              "assets/images/scrumble_open.png"),
                                                          closed_surf=ImageManager.load(
                                                              "assets/images/scrumble_closed.png"),
                                                          position=(568, 57),
                                                          name="Scrumble Rack"),
                                       Grabbable(self, ImageManager.load("assets/images/scrabble_7.png"),
                                                 name="Scrumble Tile", shadow_height=2,
                                                 position=(596, 23)),
                                   ]),
                GeometricContainer(self,
                                   ImageManager.load("assets/images/bag_of_holding_open_placeable_area.png"),
                                   draw_surf=ImageManager.load("assets/images/bag_of_holding_open.png"),
                                   closed_surf=ImageManager.load("assets/images/bag_of_holding_closed.png"),
                                   position=(525, 114),
                                   name="Bag of Holding",
                                   contents=[
                                       Grabbable(self, ImageManager.load("assets/images/dice_tin.png"),
                                                 name="Dice Tin",
                                                 position=(483, 80),
                                                 can_only_contain_tags=["Dice"],
                                                 capacity=1000),
                                       Grabbable(self, ImageManager.load("assets/images/mario.png"),
                                                 name="Swell Maurice Bros 3",
                                                 position=(552, 65), tags=["Game Cartridge"]),
                                       Grabbable(self, ImageManager.load("assets/images/lotus.png"),
                                                 name="Mox Lily",
                                                 position=(565, 132),
                                                 tags=["Game Card"], shadow_height=2),
                                       Grabbable(self, ImageManager.load("assets/images/scrabble_5.png"),
                                                 name="Scrumble Tile",
                                                 position=(523, 167), shadow_height=2),
                                       Grabbable(self, ImageManager.load("assets/images/d20.png"),
                                                 name="D20",
                                                 tags=["Dice"],
                                                 position=(481, 144)),
                                   ]),
                Grabbable(self, ImageManager.load("assets/images/scrabble_l.png"),
                          name="Scrumble Tile",
                          position=(108, 227), shadow_height=2),
                Grabbable(self, ImageManager.load("assets/images/scrabble_d.png"),
                          name="Scrumble Tile",
                          position=(390, 330), shadow_height=2),
                Grabbable(self, ImageManager.load("assets/images/ace.png"),
                          name="Ace of Spades",
                          position=(461, 302),
                          tags = ["Game Card"], shadow_height=2),
                Grabbable(self, ImageManager.load("assets/images/d8.png"),
                          name="D8",
                          tags=["Dice"],
                          position=(479, 281)),
                Grabbable(self, ImageManager.load("assets/images/pot_of_greed.png"),
                          name="Unpleasant Teapot",
                          position=(81, 82),
                          tags = ["Game Card"], shadow_height=2),
                Grabbable(self, ImageManager.load("assets/images/strike.png"),
                          name="Slash",
                          position=(45, 258),
                          tags = ["Game Card"], shadow_height=2),
                Grabbable(self, ImageManager.load("assets/images/reverse.png"),
                          name="Undo",
                          position=(578, 201),
                          tags = ["Game Card"], shadow_height=2),
                Grabbable(self, ImageManager.load("assets/images/deckbox.png"),
                          name="Deck Box",
                          position=(54, 47),
                          can_only_contain_tags=["Game Card"],
                          capacity=60),
                Grabbable(self, ImageManager.load("assets/images/play_mat.png"),
                          name="Play Mat",
                          position=(104, 259)),
                Grabbable(self, ImageManager.load("assets/images/d6.png"),
                          name="D6",
                          tags=["Dice"],
                          position=(605, 162)),
                Grabbable(self, ImageManager.load("assets/images/horseshoe.png"),
                          name="Horseshoe",
                          position=(583, 295)),
                Grabbable(self, ImageManager.load("assets/images/meeeple.png"),
                          name="Meeple",
                          position=(573, 169)),
                Grabbable(self, ImageManager.load("assets/images/dash_galaxy.png"),
                          name="Rush Universe and the Martian Hospital",
                          position=(545, 313), tags=["Game Cartridge"]),
                Grabbable(self, ImageManager.load("assets/images/duck_hunt.png"),
                          name="Goose Chase",
                          position=(595, 231), tags=["Game Cartridge"]),
                Grabbable(self, ImageManager.load("assets/images/d4.png"),
                          name="D4",
                          tags=["Dice"],
                          position=(100, 280)),
                Grabbable(self, ImageManager.load("assets/images/d12.png"),
                          name="D12",
                          tags=["Dice"],
                          position=(139, 286)),
                Grabbable(self, ImageManager.load("assets/images/monotony.png"),
                          name="Monotony Board",
                          position=(253, 331)),
                Grabbable(self, ImageManager.load("assets/images/airlock.png"),
                          name="Airlock",
                          position=(528, 220)),

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
        subtitle = ""
        if self.game.current_level == 0:
            subtitle = "Level One: Overnight"
        if self.game.current_level == 1:
            subtitle = "Level Two: Catsitting"
        if self.game.current_level == 2:
            subtitle = "Level Three: Game Night"
        self.banner_toast.show("Pack everything up!", subtitle=subtitle)

        if self.game.just_on_title_screen == True:
            self.game.just_on_title_screen = False
            self.game.main_music.play(-1)

        self.purr_sound = SoundManager.load("assets/audio/purr.ogg")
        play_purr = False
        for grabbable in self.grabbable_manager.grabbables:
            if grabbable.name == "Crouton":
                play_purr = True
                break
        if play_purr:
            self.purr_sound.set_volume(0)
            self.purr_sound.play(-1)

        if self.game.current_level == 0:
            self.backdrop = ImageManager.load("assets/images/backdrop.png")
        elif self.game.current_level == 1:
            self.backdrop = ImageManager.load("assets/images/backdrop_2.png")
        elif self.game.current_level == 2:
            self.backdrop = ImageManager.load("assets/images/backdrop_3.png")


    def update(self, dt, events):
        self.grabbable_manager.update(dt, events)
        self.banner_toast.update(dt, events)
        if (self.grabbable_manager.completed or self.grabbable_manager.restarting) and self.banner_toast.faded_to_black and not self.done:
            self.done = True
            if (self.grabbable_manager.completed):
                self.game.current_level += 1
        if (self.grabbable_manager.held_grabbable and self.grabbable_manager.held_grabbable.name == "Crouton"):
            self.purr_sound.set_volume(1)
        else:
            self.purr_sound.set_volume(0)

    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.backdrop, (int(offset[0] + c.WINDOW_WIDTH//2 - self.backdrop.get_width()//2), int(offset[1] + c.WINDOW_HEIGHT//2 - self.backdrop.get_height()//2)))
        self.grabbable_manager.draw(surface, offset)
        self.banner_toast.draw(surface, offset)

    def next_frame(self):
        self.purr_sound.stop()
        return TransitionFrame(self.game)


class TitleFrame(Frame):
    def load(self):
        self.grabbable_manager = GrabbableManager(self)

        LEVEL_TITLE = [
            Grabbable(self, ImageManager.load("assets/images/suitcase_closed_title.png"), name="Suitcase",
                      position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT // 3)),
            Grabbable(self, ImageManager.load("assets/images/crouton.png"), name="Crouton",
                      position=(c.WINDOW_WIDTH // 2, c.WINDOW_HEIGHT * 0.22), alive=True),
            Grabbable(self, ImageManager.load("assets/images/toy.png"), name="Cat Toy",
                      position=(c.WINDOW_WIDTH *5, c.WINDOW_HEIGHT * 5)),
        ]
        for item in LEVEL_TITLE:
            self.grabbable_manager.add_grabbable(item)
            item.can_be_grabbed = False
        self.banner_toast = BannerToast(self)

        self.game.current_level = 0

        self.game.title_music.play(-1)

        self.backdrop = ImageManager.load("assets/images/title_backdrop.png")
        self.continue_button = Button(
            ImageManager.load("assets/images/play_button.png"),
            (c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT - 30),
            on_click=self.proceed,
            hover_surf=ImageManager.load("assets/images/play_button_hovered.png"),
            click_surf=ImageManager.load("assets/images/play_button_clicked.png"),
        )

    def proceed(self):
        self.banner_toast.show("", fade_to_black=True, delay=1)
        self.game.shake(2)
        self.grabbable_manager.level_complete.play()
        self.game.title_music.fadeout(500)

    def update(self, dt, events):
        self.grabbable_manager.update(dt, events)
        self.banner_toast.update(dt, events)

        if self.banner_toast.faded_to_black:
            self.done = True

        self.continue_button.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.backdrop, (offset[0] + c.WINDOW_WIDTH//2 - self.backdrop.get_width()//2, offset[1] + c.WINDOW_HEIGHT//2 - self.backdrop.get_height()//2))
        self.grabbable_manager.draw(surface, offset)
        self.continue_button.draw(surface, *offset)
        self.banner_toast.draw(surface, offset)

    def next_frame(self):
        self.game.just_on_title_screen = True
        return TransitionFrame(self.game)


class ThanksFrame(Frame):
    def load(self):
        self.game.main_music.play(-1)

        self.backdrop = ImageManager.load("assets/images/end_screen_background.png")
        self.continue_button = Button(
            ImageManager.load("assets/images/menu_button.png"),
            (c.WINDOW_WIDTH//2, c.WINDOW_HEIGHT//2 - 5),
            on_click=self.proceed,
            hover_surf=ImageManager.load("assets/images/menu_button_hoveered.png"),
            click_surf=ImageManager.load("assets/images/menu_button_clicked.png"),
        )
        self.moonsigil_button = Button(
            ImageManager.load("assets/images/moonsigil_button.png"),
            (372,297),
            on_click=self.game.open_steam_page,
            hover_surf=ImageManager.load("assets/images/moonsigil_button_hover.png"),
            click_surf=ImageManager.load("assets/images/moonsigil_button_click.png"),
        )
        self.banner_toast = BannerToast(self)
        self.grabbable_manager = GrabbableManager(self)

    def proceed(self):
        self.banner_toast.show("", fade_to_black=True, delay=1)
        self.game.main_music.fadeout(500)
        self.grabbable_manager.level_complete.play()

    def update(self, dt, events):
        self.banner_toast.update(dt, events)

        if self.banner_toast.faded_to_black:
            self.done = True

        self.continue_button.update(dt, events)
        self.moonsigil_button.update(dt, events)

    def draw(self, surface, offset=(0, 0)):
        surface.blit(self.backdrop, (offset[0] + c.WINDOW_WIDTH//2 - self.backdrop.get_width()//2, offset[1] + c.WINDOW_HEIGHT//2 - self.backdrop.get_height()//2))
        self.continue_button.draw(surface, *offset)
        self.moonsigil_button.draw(surface, *offset)
        self.banner_toast.draw(surface, offset)

    def next_frame(self):
        self.game.current_level = -1
        return TransitionFrame(self.game)


class TransitionFrame(Frame):

    def load(self):
        self.age = 0
        if self.game.current_level >= 3:
            self.game.main_music.fadeout(500)

    def update(self, dt, events):
        self.age += dt
        super().update(dt, events)
        if (self.age > 2):
            self.done = True

    def draw(self, screen, offset=(0, 0)):
        screen.fill((0, 0, 0))

    def next_frame(self):
        if (self.game.current_level == -1):
            self.game.current_level = 0
            return TitleFrame(self.game)
        elif (self.game.current_level < 3):
            return PackingFrame(self.game)
        else:
            return ThanksFrame(self.game)

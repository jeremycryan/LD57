import math
import time

import pygame
import constants as c

class BannerToast:

    def __init__(self, frame):
        self.font = pygame.font.Font("assets/fonts/a_goblin_appears.ttf", size= 18)
        self.small_alert_text = pygame.font.Font("assets/fonts/smallest_pixel.ttf", size=10)
        self.small_alert_glyphs = {i: self.small_alert_text.render(i, False, (255, 255, 255)) for i in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz./'!?-_ "}
        self.small_alert_text = ""

        self.since_toast = 999
        self.toast_duration = 2
        self.showing = 0

        self.text_surf = None
        self.black = pygame.Surface(c.WINDOW_SIZE)
        self.black.fill((0, 0, 0))

        self.fade_to_black = False
        self.faded_to_black = False
        self.age = 0

    def update(self, dt, events):
        self.since_toast += dt
        self.age += dt
        through = self.since_toast/self.toast_duration
        if through >= 1:
            self.showing = 0
        else:
            self.showing = min(min(1, through * 4), (1 - through)*4)
        pass

    def draw(self, surface, offset=(0, 0)):
        through = self.since_toast/self.toast_duration
        if (through >= 1 and self.fade_to_black):
            self.faded_to_black = True
        self.black.set_alpha(max(256 - 200 * self.age, max(128 * self.showing, 512 * through - 255 if self.fade_to_black else 0)))
        if (self.black.get_alpha() > 1):
            surface.blit(self.black, (0, 0))
        if (self.showing > 0):

            squint_height = int(80 * self.showing)
            squint_surf = pygame.Surface((c.WINDOW_WIDTH, squint_height))
            squint_surf.fill((0, 0, 0))
            surface.blit(squint_surf, (0, 0))
            surface.blit(squint_surf, (0, c.WINDOW_HEIGHT - squint_height))


            banner_height = 20 + 30 * self.showing
            banner_alpha = 182 * self.showing
            banner_surf = pygame.Surface((c.WINDOW_WIDTH, banner_height))
            banner_surf.set_alpha(banner_alpha)
            #surface.blit(banner_surf, (0, c.WINDOW_HEIGHT//2 - banner_height//2))

            self.text_surf.set_alpha(255*self.showing)
            surface.blit(self.text_surf, (c.WINDOW_WIDTH//2 - self.text_surf.get_width()//2, c.WINDOW_HEIGHT//2 - self.text_surf.get_height()//2))

        if (self.small_alert_text):
            letters = [self.small_alert_glyphs[i] for i in self.small_alert_text]
            width = sum([letter.get_width() for letter in letters])
            x = c.WINDOW_WIDTH//2 - width//2
            y = c.WINDOW_HEIGHT - 15
            for letter in letters:
                surface.blit(letter, (x, y + 2 * math.sin(time.time()*3 - x/17)))
                x += letter.get_width()


        pass

    def show(self, text, fade_to_black = False):
        self.text = text
        self.since_toast = 0
        self.text_surf = self.font.render(self.text, False, (255, 255, 255))
        self.small_alert_text = ""
        self.fade_to_black = fade_to_black

    def small_alert(self, text):
        self.small_alert_text = text

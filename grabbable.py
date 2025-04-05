import math
import time

import pygame

from primitives import Pose

class Grabbable:

    def __init__(self, frame, surface, position = (0, 0)):
        self.frame = frame
        self.position = Pose(position)
        self.surface = surface
        self.update_mask()
        self.tint_surface = self.generate_tint_surface()
        self.rect = surface.get_rect()
        self.inner_grabbables = []

        self.since_pulled_out = 999
        self.pull_out_animation_length = 0.2
        self.target_position = self.position
        self.since_put_in = 999
        self.put_in_animation_length = 0.1
        self.since_put_in_me = 999
        self.put_in_me_animation_length = 0.3

        self.placeable = True

        self.inside_another = False
        self.can_be_grabbed = True
        self.is_geometric_container = False

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.surface, 10)
        self.bounding_rects = self.mask.get_bounding_rects()

    def generate_tint_surface(self):
        mask = self.mask
        tint_surf = mask.to_surface(setcolor=(255, 0, 0, 128), unsetcolor=(0, 0, 0, 0)).convert_alpha()
        return tint_surf

    def point_over_surface(self, pose):
        rect = pygame.Rect(self.position.x - self.rect.w/2, self.position.y - self.rect.h/2, self.rect.w, self.rect.h)
        if not rect.collidepoint(pose.x, pose.y):
            return False
        x_off = pose.x - rect.x
        y_off = pose.y - rect.y
        if self.surface.get_at((x_off, y_off)).a < 5:
            return False
        return True

    def set_target_position(self, pose):
        self.target_position = pose

    def update(self, dt, events):
        self.since_pulled_out += dt
        self.since_put_in += dt
        self.since_put_in_me += dt
        diff = self.target_position - self.position
        self.position += diff * dt * 10

        for grabbable in self.inner_grabbables:
            if grabbable.since_put_in < grabbable.put_in_animation_length:
                grabbable.set_target_position(self.position)
                grabbable.update(dt, events)

    def draw(self, surface, offset = (0, 0)):
        surf_to_draw = self.surface
        if not self.placeable:
            surf_to_draw = surf_to_draw.copy()
            surf_to_draw.blit(self.tint_surface, (0, 0))
        alphas = []
        scales = []
        if (self.since_pulled_out < self.pull_out_animation_length):
            through = self.since_pulled_out/self.pull_out_animation_length
            alphas.append((255 * through**0.5))
            scales.append((-(through - 0.75)**2 + 0.5625) * 2 * 0.7 + 0.3)

        if (self.since_put_in < self.put_in_animation_length):
            through = self.since_put_in/self.put_in_animation_length
            alphas.append(255 - (255 * through**0.5))
            scales.append((1 - through)**0.5)

        if (self.since_put_in_me < self.put_in_me_animation_length):
            through = self.since_put_in_me/self.put_in_me_animation_length
            scales.append(1 + 0.1 * (1 - through)**2)

        scale = 1 if not scales else sum(scales)/len(scales)
        alpha = 255 if not alphas else sum(alphas)/len(alphas)

        if (abs(scale - 1) > 0.01):
            surf_to_draw = pygame.transform.scale(self.surface, (self.surface.get_width() * scale, self.surface.get_height() * scale))

        self.surface.set_alpha(alpha)

        diff = self.target_position.x - self.position.x
        rotation = math.atan(diff/100) * 20
        if (abs(rotation) > 1):
            surf_to_draw = pygame.transform.rotate(surf_to_draw, rotation)

        x = offset[0] + self.position.x - surf_to_draw.get_width()//2
        y = offset[1] + self.position.y - surf_to_draw.get_height()//2
        surface.blit(surf_to_draw, (x, y))

        for grabbable in self.inner_grabbables:
            if grabbable.since_put_in < grabbable.put_in_animation_length:
                grabbable.draw(surface, offset)

    def try_pull_out(self):
        if self.inner_grabbables:
            result = self.inner_grabbables[-1]
            self.inner_grabbables = self.inner_grabbables[:-1]
            return result
        return None

    def can_be_put_in(self, other, position):
        return True

    def try_insert(self, other, position):
        if not self.can_be_put_in(other, position):
            return False
        self.inner_grabbables.append(other)
        other.on_put_in(self)
        return True

    @staticmethod
    def square_surface(color = (255, 255, 255), width = 100, height = 100):
        surface = pygame.Surface((width, height))
        surface.fill(color)
        return surface.convert_alpha()

    def on_pulled_out_of(self, other):
        self.since_pulled_out = 0
        self.inside_another = False
        other.on_put_in_me(self)

    def on_put_in(self, other):
        self.since_put_in = 0
        self.inside_another = True
        other.on_put_in_me(self)

    def on_put_in_me(self, other):
        self.since_put_in_me = 0

    def collides_with_other(self, other, position = None):
        if position is None:
            position = self.position
        offset = (other.position - position).get_position()
        offset = offset[0] + self.rect.w//2 - other.rect.w//2, offset[1] + self.rect.h//2 - other.rect.h//2
        return (self.mask.overlap(other.mask, offset)) is not None

    def contains_other_rect(self, other_rect, other_position, position = None):
        other_rect = other_rect.copy()
        if position is None:
            position = self.position
        offset = (other_position - position).get_position()
        offset = offset[0] + self.rect.w//2 - other_rect.w//2, offset[1] + self.rect.h//2 - other_rect.h//2
        other_rect.x += offset[0]
        other_rect.y += offset[1]
        return self.rect.contains(other_rect)


class GeometricContainer(Grabbable):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.can_be_grabbed = False
        self.associated_grabbables = []
        self.is_geometric_container = True

    def collides_with_other(self, other, position):
        if not other.collides_with_other(self, position):
            return False
        return True

    def can_have_other_put_in(self, other, position):
        if not self.collides_with_other(other, position):
            return False
        for small_rect in other.bounding_rects:
            if not self.contains_other_rect(small_rect, position, self.position):
                return False
        for already_fit in self.associated_grabbables:
            if already_fit == other:
                continue
            if other.collides_with_other(already_fit, position):
                return False
        return True

    def add_grabbable(self, grabbable):
        self.associated_grabbables.append(grabbable)
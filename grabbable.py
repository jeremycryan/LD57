import math
import time
import constants as c

import pygame

from primitives import Pose

class Grabbable:

    def __init__(self, frame, surface, name="Object", position = (0, 0), can_contain_things = False, alive = False, can_only_be_placed_in = None, can_only_contain = None, contents_must_be_smaller = False, tags=None, can_only_contain_tags = None, capacity = 1, cannot_be_placed_in_anything=False):
        self.name = name
        self.frame = frame
        self.position = Pose(position)
        self.set_surface(surface)
        self.set_draw_surface(surface)
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
        self.can_be_geometric_container = False

        self.cannot_be_placed_in_anything = cannot_be_placed_in_anything

        self.draw_outline = []
        self.outline_enabled = False

        self.can_contain_things = can_contain_things
        self.alive = alive
        if not can_only_be_placed_in:
            self.can_only_be_placed_in = []
        else:
            self.can_only_be_placed_in = can_only_be_placed_in

        self.maximum_capacity = capacity
        if not can_only_contain:
            self.can_only_contain = []
        else:
            self.can_only_contain = can_only_contain
            self.can_contain_things = True

        if not can_only_contain_tags:
            self.can_only_contain_tags = []
        else:
            self.can_only_contain_tags = can_only_contain_tags
            self.can_contain_things = True

        if not tags:
            self.tags = []
        else:
            self.tags = tags

        self.contents_must_be_smaller = contents_must_be_smaller

        self.tooltip = self.generate_tooltip()

    def generate_tooltip(self):
        sections = []
        sections.append(f"- {self.name}{' (Full)' if self.is_full() else ''} -")
        if self.can_be_geometric_container:
            sections.append("RMB to open/close")
        if self.can_contain_things and self.inner_grabbables:
            sections.append("RMB to grab contents")
        else:
            if self.name == "Catryoshka":
                sections.append("Holds one smaller Catryoshka")
        if self.can_only_be_placed_in:
            sections.append(f"Place only in {', '.join(self.can_only_be_placed_in)}")
        # if self.is_full():
        #     sections.append(f"Full")
        if self.name == "Crouton":
            sections.append("Shh... she's sleeping!")
        if self.name == "Nantucket Entertainment System":
            sections.append("Holds one game cartridge")
        if self.name == "Deck Box":
            sections.append("Holds 60 game cards")
        if self.name == "Dice Tin":
            sections.append("Holds any number of dice")
        for tag in self.tags:
            sections.append(tag)
        if self.name == "Egg of the Eternal Void":
            sections.append("Can hold any one object")
        if self.cannot_be_placed_in_anything:
            sections.append("Cannot be placed in anything")
        return sections

    def set_surface(self, surface):
        self.surface = surface
        self.update_mask()
        self.rect = surface.get_rect()

    def set_draw_surface(self, draw_surface):
        self.draw_surface = draw_surface
        draw_mask = pygame.mask.from_surface(self.draw_surface, 128)
        self.tint_surface = self.generate_tint_surface()
        self.mouseover_rect = draw_mask.get_bounding_rects()
        self.draw_outline = draw_mask.outline(2)

    def update_mask(self):
        self.mask = pygame.mask.from_surface(self.surface, 50)
        self.bounding_rects = self.mask.get_bounding_rects()

    def generate_tint_surface(self):
        mask = pygame.mask.from_surface(self.draw_surface, 10)
        tint_surf = mask.to_surface(setcolor=(255, 0, 0, 128), unsetcolor=(0, 0, 0, 0)).convert_alpha()
        return tint_surf

    def point_over_surface(self, pose):
        rect = pygame.Rect(self.position.x - self.draw_surface.get_width()//2, self.position.y - self.draw_surface.get_height()//2, self.draw_surface.get_width(), self.draw_surface.get_height())
        #rect = pygame.Rect(self.position.x - self.rect.w/2, self.position.y - self.rect.h/2, self.rect.w, self.rect.h)
        if not rect.collidepoint(pose.x, pose.y):
            return False
        x_off = pose.x - rect.x
        y_off = pose.y - rect.y
        if self.draw_surface.get_at((x_off, y_off)).a < 5:
            return False
        return True

    def set_target_position(self, pose):
        if pose.x < 0:
            pose.x = 0
        if pose.y < 0:
            pose.y = 0
        if pose.x > c.WINDOW_WIDTH:
            pose.x = c.WINDOW_WIDTH
        if pose.y > c.WINDOW_HEIGHT:
            pose.y = c.WINDOW_HEIGHT
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

    def draw_rects(self, surface, offset=(0, 0)):
        for rect in self.bounding_rects:
            x = offset[0] + rect.x + self.position.x - self.rect.w//2
            y = offset[1] + rect.y + self.position.y - self.rect.h//2
            pygame.draw.rect(surface, (255, 0, 0), (x, y, rect.w, rect.h), width=2)
        pygame.draw.rect(surface, (0, 0, 255), (self.position.x - self.rect.w//2, self.position.y - self.rect.h//2, self.rect.w, self.rect.h), width = 2)

    def draw(self, surface, offset = (0, 0)):
        surf_to_draw = self.draw_surface
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
        x_scale = scale
        y_scale = scale
        if self.alive:
            factor = 1 + math.sin(time.time() * 1.5)*0.010
            #x_scale *= factor
            y_scale /= factor

        if (abs(x_scale - 1) > 0.01) or (abs(y_scale - 1) > 0.005):
            surf_to_draw = pygame.transform.scale(surf_to_draw, (surf_to_draw.get_width() * x_scale, surf_to_draw.get_height() * y_scale))

        surf_to_draw.set_alpha(alpha)

        diff = self.target_position.x - self.position.x
        rotation = math.atan(diff/100) * 20
        if (abs(rotation) > 1):
            surf_to_draw = pygame.transform.rotate(surf_to_draw, rotation)

        x = int(offset[0] + self.position.x - surf_to_draw.get_width()//2)
        y = int(offset[1] + self.position.y - surf_to_draw.get_height()//2)
        # if self.outline_enabled:
        #     self.draw_outline = pygame.mask.from_surface(surf_to_draw).outline(2)
        #     if self.draw_outline:
        #         pygame.draw.polygon(
        #             surface,
        #             (255, 255, 255),
        #             [(i[0] + x, i[1] + y) for i in self.draw_outline],
        #             width=3
        #         )
        surface.blit(surf_to_draw, (x, y))

        for grabbable in self.inner_grabbables:
            if grabbable.since_put_in < grabbable.put_in_animation_length:
                grabbable.draw(surface, offset)



        #self.draw_rects(surface, offset)

    def try_pull_out(self):
        if self.inner_grabbables:
            result = self.inner_grabbables[-1]
            self.inner_grabbables = self.inner_grabbables[:-1]
            return result
        return None

    def is_smaller_than(self, other):
        return self.rect.w <= other.rect.w and self.rect.h <= other.rect.h

    def can_be_put_in(self, other, position = None):
        if not other.can_contain_things:
            return False
        if self.cannot_be_placed_in_anything:
            return False
        if other.can_only_contain and self.name not in other.can_only_contain:
            return False
        if other.can_only_contain_tags and not any([tag in other.can_only_contain_tags for tag in self.tags]):
            return False
        if other.is_full():
            return False
        if other.contents_must_be_smaller and not self.is_smaller_than(other):
            return False
        if (not other.can_be_geometric_container):
            return True
        return False

    def is_full(self):
        return self.maximum_capacity <= len(self.inner_grabbables)

    def try_insert(self, other, position):
        if not other.can_be_put_in(self, position):
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

    def contains_other_rect(self, other_rect, other_rect_full, other_position, position = None):
        other_rect = other_rect.copy()
        if position is None:
            position = self.position
        offset = (other_position - position).get_position()
        main_rect = self.bounding_rects[0]
        offset = offset[0] + self.rect.w//2 - other_rect_full.w//2, offset[1] + self.rect.h//2 - other_rect_full.h//2
        other_rect.x += offset[0]
        other_rect.y += offset[1]
        return main_rect.contains(other_rect)

    def interact(self):
        pass

class GeometricContainer(Grabbable):
    def __init__(self, *args, draw_surf = None, is_suitcase = False, closed_surf = None, contents = None, **kwargs):
        super().__init__(*args, **kwargs)

        draw_surf = draw_surf if draw_surf is not None else self.surface
        self.original_draw_surf = draw_surf

        self.set_draw_surface(draw_surf)
        self.can_be_grabbed = False
        self.associated_grabbables = []
        if contents:
            for item in contents:
                self.associated_grabbables.append(item)
        self.is_geometric_container = True
        self.can_be_geometric_container = True
        self.closed_surf = closed_surf if closed_surf else draw_surf
        self.original_surface = self.surface
        self.is_suitcase = is_suitcase

        self.position_closed_at = self.position
        if not is_suitcase:
            self.toggle_container()

        self.tooltip = self.generate_tooltip()

    def get_count_of_grabbables_recursive(self):
        if not self.is_geometric_container:
            return 0
        count = len(self.associated_grabbables)
        for item in self.associated_grabbables:
            if item.is_geometric_container:
                count += item.get_count_of_grabbables_recursive()
        return count

    def collides_with_other(self, other, position):
        if self.can_be_grabbed:
            return Grabbable.collides_with_other(self, other, position)
        if not other.collides_with_other(self, position):
            return False
        return True

    def can_have_other_put_in(self, other, position):
        if other.cannot_be_placed_in_anything:
            return False
        if (other.can_only_be_placed_in):
            if not self.name in other.can_only_be_placed_in:
                return False
        if not other.collides_with_other(self, position):
            return False
        for small_rect in other.bounding_rects:
            if not self.contains_other_rect(small_rect, other.rect, position, self.position):
                return False
        for already_fit in self.associated_grabbables:
            if already_fit == other:
                continue
            if other.collides_with_other(already_fit, position):
                return False
        return True

    def add_grabbable(self, grabbable):
        self.associated_grabbables.append(grabbable)

    def toggle_container(self, items_to_remove = None):
        if (self.is_geometric_container):
            self.is_geometric_container = False
            self.can_be_grabbed = True
            self.set_draw_surface(self.closed_surf)
            self.position_closed_at = self.target_position.copy()

            for grabbable in self.associated_grabbables:
                if (items_to_remove is not None):
                    items_to_remove.append(grabbable)
                if grabbable.is_geometric_container:
                    grabbable.toggle_container(items_to_remove)
            self.set_surface(self.closed_surf)
        else:
            self.is_geometric_container = True
            self.can_be_grabbed = False
            self.set_draw_surface(self.original_draw_surf)

            for grabbable in self.associated_grabbables:
                grabbable.target_position += self.target_position - self.position_closed_at
                grabbable.position = grabbable.target_position
                grabbable.on_pulled_out_of(self)

            self.set_surface(self.original_surface)
        self.on_put_in_me(None)

    def interact(self, items_to_remove = None, items_to_add = None):
        if self.is_geometric_container:
            for item in self.associated_grabbables:
                if (items_to_remove is not None):
                    items_to_remove.append(item)
        else:
            for item in self.associated_grabbables:
                if (items_to_add is not None):
                    items_to_add.append(item)
        self.toggle_container(items_to_remove)
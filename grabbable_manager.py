import pygame

from primitives import Pose
import constants as c
from sound_manager import SoundManager


class GrabbableManager:

    def __init__(self, frame):
        self.frame = frame
        self.grabbables = []
        self.held_grabbable = None
        self.current_mouse_position = Pose((0, 0))
        self.grabbable_offset = Pose((0, 0))
        self.original_grab_position = Pose((0, 0))
        self.original_grab_container = None
        self.original_valid_geometric_container = None

        self.tooltip_font = pygame.font.Font("assets/fonts/smallest_pixel.ttf", 10)
        self.tooltip_surf = pygame.Surface((10, 10))
        self.tooltip_grabbable = None

        self.completed = False
        self.since_completed = 0
        self.completed_sound_played = False
        self.restarting = False

        self.level_complete = SoundManager.load("assets/audio/level_complete.ogg")

    def add_grabbables(self, *args):
        for arg in args:
            self.add_grabbable(arg)

    def add_grabbable(self, grabbable):
        if (grabbable in self.grabbables):
            self.move_to_front(grabbable)
        else:
            self.grabbables.append(grabbable)

    def remove_grabbable(self, grabbable):
        if grabbable in self.grabbables:
            self.grabbables.remove(grabbable)

    def move_to_front(self, grabbable):
        if (grabbable in self.grabbables):
            self.remove_grabbable(grabbable)
            self.add_grabbable(grabbable)

    def update(self, dt, events):
        self.current_mouse_position = Pose(pygame.mouse.get_pos()) * (1/c.WINDOW_SCALE)
        if self.held_grabbable:
            self.held_grabbable.set_target_position(self.current_mouse_position + self.grabbable_offset)


        for grabbable in self.grabbables:
            grabbable.update(dt, events)

        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.try_pick_up()
                    break
                if event.button == 3 and not self.held_grabbable:
                    self.try_pull_out()
                    break
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.frame.banner_toast.show("Restarting Level!", fade_to_black=True, delay=0)
                    self.frame.game.shake(2)
                    self.restarting = True

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    self.try_drop()

        self.update_held_grabbable_placeability()
        if (self.everything_is_packed()) and not self.completed:
            self.completed = True
            self.frame.banner_toast.show("Level complete!", fade_to_black = True, delay=-1)
            self.frame.game.shake(2)

        if self.completed:
            self.since_completed += dt
            if not self.completed_sound_played and self.since_completed > 1.25:
                self.level_complete.play()
                self.completed_sound_played = True

        self.set_tooltip_grabbable()

        for grabbable in self.grabbables:
            grabbable.outline_enabled = False
        if self.tooltip_grabbable:
            self.tooltip_grabbable.outline_enabled = True

    def update_held_grabbable_placeability(self, use_mouse_position = False):
        for grabbable in self.grabbables:
            grabbable.placeable = True
        valid_placement = True
        if self.held_grabbable:
            hovered = self.grabbable_under_mouse_position(include_held=False, must_be_grabbable=False)
            if hovered and self.held_grabbable.can_be_put_in(hovered):
                pass
            else:
                position_to_check = self.held_grabbable.position if not use_mouse_position else self.current_mouse_position + self.grabbable_offset
                valid_placement_override = False
                valid_placement = True
                for geometric_container in self.grabbables[::-1]:
                    if not geometric_container.is_geometric_container:
                        continue
                    if not geometric_container.collides_with_other(self.held_grabbable, position_to_check):
                        continue
                    if not geometric_container.can_have_other_put_in(self.held_grabbable, position_to_check):
                        self.held_grabbable.placeable = False
                        valid_placement = False
                    break
                if valid_placement or valid_placement_override:
                    self.original_grab_position = position_to_check
                    under = self.grabbable_under_position(position_to_check, include_held=False, must_be_grabbable=False)
                    if under and under.is_geometric_container and under.can_have_other_put_in(self.held_grabbable, position_to_check):
                        self.original_valid_geometric_container = under
                    else:
                        self.original_valid_geometric_container = None

    def draw(self, surf, offset=(0, 0)):
        for grabbable in self.grabbables:
            grabbable.draw(surf, offset)
        if self.tooltip_grabbable:
            position = self.current_mouse_position + Pose((4, 2))
            surf.blit(self.tooltip_surf, position.get_position())


    def grabbable_under_mouse_position(self, include_held = True, must_be_grabbable = True):
        position = self.current_mouse_position
        return self.grabbable_under_position(position, include_held=include_held, must_be_grabbable=must_be_grabbable)

    def grabbable_under_position(self, position, include_held = True, must_be_grabbable = True):
        for grabbable in self.grabbables[::-1]:
            if (must_be_grabbable and not grabbable.can_be_grabbed):
                continue
            if not include_held and grabbable == self.held_grabbable:
                continue
            if (grabbable.point_over_surface(position)):
                return grabbable
        return None

    def set_tooltip_grabbable(self):
        if self.held_grabbable:
            self.tooltip_grabbable = None
            return
        grabbable = self.grabbable_under_mouse_position(must_be_grabbable=False)
        if self.tooltip_grabbable != grabbable:
            self.tooltip_grabbable = grabbable
            self.update_tooltip_surf()

    def update_tooltip_surf(self):

        if self.tooltip_grabbable == None:
            return
        self.tooltip_grabbable.tooltip = self.tooltip_grabbable.generate_tooltip()
        text = self.tooltip_grabbable.tooltip
        lines = [self.tooltip_font.render(line, False, (255, 255, 255)) for line in text]
        height = sum([i.get_height() for i in lines])
        width = max([i.get_width() for i in lines])
        surf = pygame.Surface((width + 8, height + 8)).convert_alpha()
        surf.fill((0, 0, 0, 128))
        x = 4
        y = 4
        for line in lines:
            surf.blit(line, (x, y))
            y += line.get_height()
        self.tooltip_surf = surf

    def try_pick_up(self):
        grabbable = self.grabbable_under_mouse_position()
        if grabbable:
            self.pick_up(grabbable)

    def try_pull_out(self):
        if self.completed:
            return
        container = self.grabbable_under_mouse_position(must_be_grabbable=False)
        if not container:
            self.original_grab_container = None
            return
        if container.can_be_geometric_container:
            items_to_remove = []
            items_to_add = []
            container.interact(items_to_remove, items_to_add)
            self.move_to_front(container)
            for item in items_to_remove:
                self.remove_grabbable(item)
            for item in items_to_add:
                self.add_grabbable(item)
            return
        grabbable = container.try_pull_out()
        if not grabbable:
            self.original_grab_container = None
            return
        self.add_grabbable(grabbable)
        self.held_grabbable = grabbable
        self.held_grabbable.position = self.current_mouse_position
        self.grabbable_offset = Pose((0, 0))
        grabbable.on_pulled_out_of(container)
        self.original_grab_container = container

    def pick_up(self, grabbable):
        grabbable.on_become_held()
        self.original_grab_container = None
        self.move_to_front(grabbable)
        self.held_grabbable = grabbable
        self.grabbable_offset = grabbable.position - self.current_mouse_position
        #self.original_grab_position = self.held_grabbable.position

    def remove_from_all_geometric_containers(self, grabbable):
        for potential_container in self.grabbables:
            if potential_container.is_geometric_container:
                if grabbable in potential_container.associated_grabbables:
                    potential_container.associated_grabbables.remove(grabbable)

    def try_drop(self):
        container = self.grabbable_under_mouse_position(include_held=False, must_be_grabbable=False)
        put_in_geometric_container = False

        if container and not container.can_be_geometric_container and self.held_grabbable and container.try_insert(self.held_grabbable, self.current_mouse_position):
            self.remove_grabbable(self.held_grabbable)
            self.remove_from_all_geometric_containers(self.held_grabbable)
            self.held_grabbable = None
            return

        self.update_held_grabbable_placeability(True)
        if self.held_grabbable and not self.held_grabbable.placeable:
            self.held_grabbable.target_position = self.original_grab_position
            if self.original_grab_container:
                if self.original_grab_container.try_insert(self.held_grabbable, self.original_grab_container.position):
                    self.original_grab_container = None
                    self.remove_grabbable(self.held_grabbable)
            elif self.original_valid_geometric_container:
                if self.original_valid_geometric_container.can_have_other_put_in(self.held_grabbable, self.held_grabbable.target_position):
                    self.remove_from_all_geometric_containers(self.held_grabbable)
                    self.original_valid_geometric_container.add_grabbable(self.held_grabbable)
            else:
                self.remove_from_all_geometric_containers(self.held_grabbable)
            self.held_grabbable.on_placed()
            self.held_grabbable = None
            return

        if container and container.is_geometric_container:
            if self.held_grabbable and container.can_have_other_put_in(self.held_grabbable, self.current_mouse_position + self.grabbable_offset):
                self.remove_from_all_geometric_containers(self.held_grabbable)
                container.add_grabbable(self.held_grabbable)
                put_in_geometric_container = True

        if not put_in_geometric_container:
            self.remove_from_all_geometric_containers(self.held_grabbable)

        if self.held_grabbable:
            self.held_grabbable.on_put_in_me(None)
            self.held_grabbable.on_placed()
        self.held_grabbable = None


    def everything_is_packed(self):
        if len(self.grabbables) == 1:
            return True
        almost_won = False
        for container in self.grabbables[:]:
            if container.is_geometric_container:
                if container.get_count_of_grabbables_recursive() + 1 == len(self.grabbables):
                    almost_won = True
        if almost_won:
            self.frame.banner_toast.small_alert("Close your suitcase!")
        else:
            self.frame.banner_toast.small_alert("")
        return False
import pygame

from primitives import Pose
import constants as c


class GrabbableManager:

    def __init__(self, frame):
        self.frame = frame
        self.grabbables = []
        self.held_grabbable = None
        self.current_mouse_position = Pose((0, 0))
        self.grabbable_offset = Pose((0, 0))
        self.original_grab_position = Pose((0, 0))

    def add_grabbables(self, *args):
        for arg in args:
            self.add_grabbable(arg)

    def add_grabbable(self, grabbable):
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
                if event.button == 3:
                    self.try_pull_out()

        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1 or event.button == 3:
                    self.try_drop()

        self.update_held_grabbable_placeability()

    def update_held_grabbable_placeability(self, use_mouse_position = False):
        for grabbable in self.grabbables:
            grabbable.placeable = True
        valid_placement = True
        if self.held_grabbable:
            position_to_check = self.held_grabbable.position if not use_mouse_position else self.current_mouse_position + self.grabbable_offset
            for geometric_container in self.grabbables:
                if not geometric_container.is_geometric_container:
                    continue
                if not geometric_container.collides_with_other(self.held_grabbable, position_to_check):
                    continue
                if not geometric_container.can_have_other_put_in(self.held_grabbable, position_to_check):
                    self.held_grabbable.placeable = False
                    valid_placement = False
            if valid_placement:
                self.original_grab_position = position_to_check

    def draw(self, surf, offset=(0, 0)):
        for grabbable in self.grabbables:
            grabbable.draw(surf, offset)

    def grabbable_under_mouse_position(self, include_held = True, must_be_grabbable = True):
        position = self.current_mouse_position
        # Convert to world space?
        for grabbable in self.grabbables[::-1]:
            if (must_be_grabbable and not grabbable.can_be_grabbed):
                continue
            if not include_held and grabbable == self.held_grabbable:
                continue
            if (grabbable.point_over_surface(position)):
                return grabbable
        return None

    def try_pick_up(self):
        grabbable = self.grabbable_under_mouse_position()
        if grabbable:
            self.pick_up(grabbable)

    def try_pull_out(self):
        container = self.grabbable_under_mouse_position()
        if not container:
            return
        grabbable = container.try_pull_out()
        if not grabbable:
            return
        self.add_grabbable(grabbable)
        self.held_grabbable = grabbable
        self.held_grabbable.position = self.current_mouse_position
        self.grabbable_offset = Pose((0, 0))
        grabbable.on_pulled_out_of(container)

    def pick_up(self, grabbable):
        self.move_to_front(grabbable)
        self.held_grabbable = grabbable
        self.grabbable_offset = grabbable.position - self.current_mouse_position
        self.original_grab_position = self.held_grabbable.position

    def remove_from_all_geometric_containers(self, grabbable):
        for potential_container in self.grabbables:
            if potential_container.is_geometric_container:
                if grabbable in potential_container.associated_grabbables:
                    potential_container.associated_grabbables.remove(grabbable)

    def try_drop(self):
        container = self.grabbable_under_mouse_position(include_held=False, must_be_grabbable=False)
        put_in_geometric_container = False

        self.update_held_grabbable_placeability(True)
        if self.held_grabbable and not self.held_grabbable.placeable:
            self.held_grabbable.target_position = self.original_grab_position
            self.held_grabbable = None
            return;

        if container and container.is_geometric_container:
            if self.held_grabbable and container.can_have_other_put_in(self.held_grabbable, self.current_mouse_position + self.grabbable_offset):
                container.add_grabbable(self.held_grabbable)
                put_in_geometric_container = True
        elif container and self.held_grabbable and container.try_insert(self.held_grabbable, self.current_mouse_position):
            self.remove_grabbable(self.held_grabbable)

        if not put_in_geometric_container:
            self.remove_from_all_geometric_containers(self.held_grabbable)

        self.held_grabbable = None
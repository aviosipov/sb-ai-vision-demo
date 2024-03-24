import pygame
from shared.scene_utils import handle_scene_restart

class AnimationEditorEventHandler:
    def __init__(self, animation_editor):
        self.animation_editor = animation_editor

    def handle_events(self, event):
        handle_scene_restart(event, self.animation_editor.reset)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.animation_editor.next_scene = "start_game"
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.animation_editor.save_animation_data()
            elif event.key == pygame.K_x and self.animation_editor.hovered_waypoint is not None:
                self.animation_editor.delete_selected_waypoint()
            elif event.key == pygame.K_a:
                self.animation_editor.add_waypoint(pygame.mouse.get_pos())
            elif event.key == pygame.K_LEFT:
                self.animation_editor.frame_control.start_frame_change(-1)
            elif event.key == pygame.K_RIGHT:
                self.animation_editor.frame_control.start_frame_change(1)
            elif event.key == pygame.K_HOME:
                self.animation_editor.frame_control.set_frame(1)
            elif event.key == pygame.K_END:
                self.animation_editor.frame_control.set_frame(60)
            elif event.key == pygame.K_SPACE:
                self.animation_editor.frame_control.toggle_play_mode()
            elif event.key == pygame.K_UP:
                self.animation_editor.selected_object = (self.animation_editor.selected_object - 1) % len(self.animation_editor.animation_data.objects)
            elif event.key == pygame.K_DOWN:
                self.animation_editor.selected_object = (self.animation_editor.selected_object + 1) % len(self.animation_editor.animation_data.objects)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.animation_editor.frame_control.stop_frame_change()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.animation_editor.start_dragging_waypoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.animation_editor.stop_dragging_waypoint()
                self.animation_editor.update_animation_data()
        elif event.type == pygame.MOUSEMOTION:
            self.animation_editor.update_hovered_waypoint(event.pos)
            if self.animation_editor.dragged_waypoint is not None:
                self.animation_editor.drag_waypoint(event.pos)
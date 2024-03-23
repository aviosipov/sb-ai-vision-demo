import pygame
import numpy as np
from shared import game_settings as settings
from shared.scene import Scene
from shared.ui import draw_rectangle
from shared.scene_utils import handle_scene_restart
from shared.path_utils import create_smooth_path
import json
from editor.timeline import Timeline
from editor.frame_control import FrameControl


class AnimationEditor(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.background_image = pygame.image.load('assets/start_game/game-intro.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.editing_mode = True
        self.selected_animation = 0
        self.animations = self.create_animations()
        self.load_animations()
        self.dragged_waypoint = None
        self.hovered_waypoint = None
        self.timelines = [Timeline(i) for i in range(len(self.animations))]
        self.frame_control = FrameControl()

    def create_animations(self):
        paths = [
            np.array([[100, 100], [200, 200], [300, 150], [400, 250]]),
            np.array([[400, 100], [300, 200], [200, 150], [100, 250]]),
            np.array([[200, 50], [300, 100], [400, 200], [300, 300]])
        ]

        animations = [{"path": path} for path in paths]
        return animations

    def reset(self):
        pass

    def handle_events(self, event):
        handle_scene_restart(event, self.reset)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_scene = "start_game"
            elif event.key == pygame.K_s:
                self.save_animations()
            elif event.key == pygame.K_r:
                self.load_animations()
            elif event.key == pygame.K_x and self.hovered_waypoint is not None:
                self.delete_selected_waypoint()
            elif event.key == pygame.K_a:
                self.add_waypoint(pygame.mouse.get_pos())
            elif event.key == pygame.K_LEFT:
                self.frame_control.start_frame_change(-1)
            elif event.key == pygame.K_RIGHT:
                self.frame_control.start_frame_change(1)
            elif event.key == pygame.K_HOME:
                self.frame_control.set_frame(1)
            elif event.key == pygame.K_END:
                self.frame_control.set_frame(60)
            elif event.key == pygame.K_SPACE:
                self.frame_control.toggle_play_mode()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.frame_control.stop_frame_change()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.start_dragging_waypoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.stop_dragging_waypoint()
        elif event.type == pygame.MOUSEMOTION:
            self.update_hovered_waypoint(event.pos)
            if self.dragged_waypoint is not None:
                self.drag_waypoint(event.pos)


    def update_hovered_waypoint(self, pos):
        animation = self.animations[self.selected_animation]
        distances = np.linalg.norm(animation['path'] - pos, axis=1)
        nearest_index = np.argmin(distances)

        if distances[nearest_index] <= 10:  # Adjust the threshold as needed
            self.hovered_waypoint = nearest_index
        else:
            self.hovered_waypoint = None

    def update(self, dt):
        self.frame_control.update(dt)


    def draw(self):
        self.screen.fill(settings.BLACK)
        self.screen.blit(self.background, (0, 0))

        for i in range(len(self.animations)):
            self.draw_path(i)
            self.draw_waypoints(i)

        self.draw_object_labels()
        self.draw_timelines()
        self.frame_control.draw(self.screen)

    def draw_object_labels(self):
        font = pygame.font.Font(None, 24)
        for i, _ in enumerate(self.animations):
            color = settings.RED if i == self.selected_animation else settings.WHITE
            text = font.render(f"Object {i+1}", True, color)
            text_rect = text.get_rect(topleft=(10, 10 + i * 30))
            self.screen.blit(text, text_rect)

    def draw_timelines(self):
        for i, timeline in enumerate(self.timelines):
            timeline.draw(self.screen, i, self.frame_control.current_frame)

    def save_animations(self):
        animation_data = [{"path": animation['path'].tolist()} for animation in self.animations]
        with open("animation_data.json", "w") as file:
            json.dump(animation_data, file)

    def load_animations(self):
        try:
            with open("animation_data.json", "r") as file:
                animation_data = json.load(file)

            for i, data in enumerate(animation_data):
                self.animations[i]['path'] = np.array(data["path"])
                self.animations[i]['smooth_path'] = create_smooth_path(self.animations[i]['path'])
        except FileNotFoundError:
            pass

    def add_waypoint(self, pos):
        self.animations[self.selected_animation]['path'] = np.append(self.animations[self.selected_animation]['path'], [pos], axis=0)
        self.animations[self.selected_animation]['smooth_path'] = create_smooth_path(self.animations[self.selected_animation]['path'])

    def delete_selected_waypoint(self):
        animation = self.animations[self.selected_animation]
        if self.hovered_waypoint is not None:
            animation['path'] = np.delete(animation['path'], self.hovered_waypoint, axis=0)
            if len(animation['path']) >= 2:  # Check if there are enough points
                animation['smooth_path'] = create_smooth_path(animation['path'])
            else:
                animation['smooth_path'] = animation['path']  # If there are less than 2 points, set smooth_path to path
            self.hovered_waypoint = None

    def start_dragging_waypoint(self, pos):
        animation = self.animations[self.selected_animation]
        distances = np.linalg.norm(animation['path'] - pos, axis=1)
        nearest_index = np.argmin(distances)

        if distances[nearest_index] <= 10:  # Adjust the threshold as needed
            self.dragged_waypoint = nearest_index

    def stop_dragging_waypoint(self):
        self.dragged_waypoint = None

    def drag_waypoint(self, pos):
        animation = self.animations[self.selected_animation]
        animation['path'][self.dragged_waypoint] = pos
        animation['smooth_path'] = create_smooth_path(animation['path'])

    def draw_waypoints(self, animation_index):
        animation = self.animations[animation_index]
        for i, waypoint in enumerate(animation['path']):
            color = settings.YELLOW
            if animation_index == self.selected_animation:
                if i == self.dragged_waypoint:
                    color = settings.ORANGE
                elif i == self.hovered_waypoint:
                    color = settings.RED
            pygame.draw.circle(self.screen, color, waypoint, 8)

    def draw_path(self, animation_index):
        animation = self.animations[animation_index]
        if len(animation['path']) >= 2:
            color = settings.WHITE if animation_index == self.selected_animation else settings.GREY
            pygame.draw.lines(self.screen, color, False, animation['smooth_path'], 2)
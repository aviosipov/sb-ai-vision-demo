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
from editor.animation_data import AnimationData

class AnimationEditor(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.background_image = pygame.image.load('assets/start_game/game-intro.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.editing_mode = True
        self.selected_object = 0
        self.load_animation_data()  # Load the animation data
        self.dragged_waypoint = None
        self.hovered_waypoint = None
        self.timelines = [Timeline(i) for i in range(len(self.animation_data.objects))]
        self.frame_control = FrameControl()


    def create_animation_data(self):
        # Create initial animation data with empty keyframes
        objects = [
            {"name": "Player", "imagePath": "player.png", "keyframes": []},
            {"name": "Enemy", "imagePath": "enemy.png", "keyframes": []}
        ]
        return AnimationData("ExampleAnimation", 2.0, 60, objects)



    def reset(self):
        pass

    def handle_events(self, event):
        handle_scene_restart(event, self.reset)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.next_scene = "start_game"
            elif event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                self.save_animation_data()  # Save the animation data when Ctrl+S is pressed
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
            elif event.key == pygame.K_UP:
                self.selected_object = (self.selected_object - 1) % len(self.animation_data.objects)
            elif event.key == pygame.K_DOWN:
                self.selected_object = (self.selected_object + 1) % len(self.animation_data.objects)
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                self.frame_control.stop_frame_change()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                self.start_dragging_waypoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                self.stop_dragging_waypoint()
                self.update_animation_data()  # Update animation data after dragging waypoint
        elif event.type == pygame.MOUSEMOTION:
            self.update_hovered_waypoint(event.pos)
            if self.dragged_waypoint is not None:
                self.drag_waypoint(event.pos)



    def update_animation_data(self):
        if self.dragged_waypoint is not None:
            object_data = self.animation_data.objects[self.selected_object]
            keyframe_data = object_data["keyframes"]

            # Find the keyframe corresponding to the current frame
            keyframe = next((kf for kf in keyframe_data if kf["frameNumber"] == self.frame_control.current_frame), None)

            if keyframe is None:
                # If there is no keyframe at the current frame, create a new keyframe
                keyframe = {
                    "frameNumber": self.frame_control.current_frame,
                    "position": list(self.get_waypoint_position(self.dragged_waypoint)),
                    "scale": [1, 1],
                    "rotation": 0,
                    "opacity": 1.0
                }
                keyframe_data.append(keyframe)
            else:
                # Update the position of the existing keyframe
                keyframe["position"] = list(self.get_waypoint_position(self.dragged_waypoint))

            # Sort the keyframes by frame number
            keyframe_data.sort(key=lambda kf: kf["frameNumber"])




    def get_waypoint_position(self, waypoint_index):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if waypoint_index < len(keyframe_data):
            return keyframe_data[waypoint_index]["position"]
        else:
            return (0, 0)  # Default position if waypoint index is out of range

    def update_hovered_waypoint(self, pos):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if len(keyframe_data) > 0:
            positions = np.array([kf["position"] for kf in keyframe_data])
            pos_array = np.array(pos)
            distances = np.linalg.norm(positions - pos_array, axis=1)
            nearest_index = np.argmin(distances)

            if distances[nearest_index] <= 10:  # Adjust the threshold as needed
                self.hovered_waypoint = nearest_index
            else:
                self.hovered_waypoint = None
        else:
            self.hovered_waypoint = None



    def update(self, dt):
        self.frame_control.update(dt)


    def draw(self):
        self.screen.fill(settings.BLACK)
        self.screen.blit(self.background, (0, 0))

        for i in range(len(self.animation_data.objects)):
            self.draw_path(i)
            self.draw_waypoints(i)

        self.draw_object_labels()
        self.draw_timelines()
        self.frame_control.draw(self.screen)

    def draw_object_labels(self):
        font = pygame.font.Font(None, 24)
        for i, obj in enumerate(self.animation_data.objects):
            color = settings.RED if i == self.selected_object else settings.WHITE
            text = font.render(f"{obj['name']}", True, color)
            text_rect = text.get_rect(topleft=(10, 10 + i * 30))
            self.screen.blit(text, text_rect)

    def draw_timelines(self):
        for i, timeline in enumerate(self.timelines):
            timeline.draw(self.screen, i, self.frame_control.current_frame, self.animation_data.objects[i]["keyframes"])

        # Draw the current frame indicator
        current_frame_x = self.frame_control.current_frame * (settings.SCREEN_WIDTH - 40) // self.frame_control.max_frame + 20
        pygame.draw.line(self.screen, settings.RED, (current_frame_x, 10), (current_frame_x, 30), 2)


    def load_animation_data(self):
        try:
            with open("animation_data.json", "r") as file:
                data = json.load(file)
                if isinstance(data, dict):
                    self.animation_data = AnimationData(data.get("name", ""), data.get("duration", 0.0), data.get("frame_rate", 0), data.get("objects", []))
                else:
                    print("Invalid animation data format. Using default values.")
                    self.animation_data = self.create_animation_data()
        except FileNotFoundError:
            print("Animation data file not found. Using default values.")
            self.animation_data = self.create_animation_data()
    

    def save_animation_data(self):
        data = {
            "name": self.animation_data.name,
            "duration": self.animation_data.duration,
            "frame_rate": self.animation_data.frame_rate,
            "objects": self.animation_data.objects
        }
        with open("animation_data.json", "w") as file:
            json.dump(data, file)



    def add_waypoint(self, pos):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        keyframe = {
            "frameNumber": self.frame_control.current_frame,
            "position": list(pos),
            "scale": [1, 1],
            "rotation": 0,
            "opacity": 1.0
        }
        keyframe_data.append(keyframe)
        keyframe_data.sort(key=lambda kf: kf["frameNumber"])

    def delete_selected_waypoint(self):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if self.hovered_waypoint is not None and self.hovered_waypoint < len(keyframe_data):
            del keyframe_data[self.hovered_waypoint]
            self.hovered_waypoint = None



    def start_dragging_waypoint(self, pos):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if len(keyframe_data) > 0:
            positions = np.array([kf["position"] for kf in keyframe_data])
            pos_array = np.array(pos)
            distances = np.linalg.norm(positions - pos_array, axis=1)
            nearest_index = np.argmin(distances)

            if distances[nearest_index] <= 10:  # Adjust the threshold as needed
                self.dragged_waypoint = nearest_index



    def stop_dragging_waypoint(self):
        self.dragged_waypoint = None

    def drag_waypoint(self, pos):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if self.dragged_waypoint is not None and self.dragged_waypoint < len(keyframe_data):
            keyframe_data[self.dragged_waypoint]["position"] = list(pos)

    def draw_waypoints(self, object_index):
        object_data = self.animation_data.objects[object_index]
        keyframe_data = object_data["keyframes"]

        # Find the keyframe corresponding to the current frame
        keyframe = next((kf for kf in keyframe_data if kf["frameNumber"] == self.frame_control.current_frame), None)

        if keyframe is None:
            # If there is no keyframe at the current frame, find the latest keyframe before the current frame
            prev_keyframes = [kf for kf in keyframe_data if kf["frameNumber"] < self.frame_control.current_frame]
            if prev_keyframes:
                keyframe = max(prev_keyframes, key=lambda kf: kf["frameNumber"])

        if keyframe is not None:
            color = settings.YELLOW
            if object_index == self.selected_object:
                if self.dragged_waypoint is not None:
                    color = settings.ORANGE
                elif self.hovered_waypoint is not None:
                    color = settings.RED
            pygame.draw.circle(self.screen, color, keyframe["position"], 8)



    def draw_path(self, object_index):
        object_data = self.animation_data.objects[object_index]
        keyframe_data = object_data["keyframes"]

        if len(keyframe_data) >= 2:
            color = settings.WHITE if object_index == self.selected_object else settings.GREY
            path = np.array([kf["position"] for kf in keyframe_data])
            smooth_path = create_smooth_path(path)
            pygame.draw.lines(self.screen, color, False, smooth_path, 2)
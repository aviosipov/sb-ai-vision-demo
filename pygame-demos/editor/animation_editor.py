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
from editor.animation_editor_event_handler import AnimationEditorEventHandler
from editor.animation_data_manager import AnimationDataManager
from editor.waypoint_manager import WaypointManager

class AnimationEditor(Scene):
    def __init__(self, screen):
        super().__init__(screen)        
        self.animation_data_manager = AnimationDataManager()
        self.animation_data_manager.load_animation_data()
        self.waypoint_manager = WaypointManager(self)
        self.screen = screen
        self.background_image = pygame.image.load('assets/start_game/game-intro.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.editing_mode = True
        self.selected_object = 0       
        self.dragged_waypoint = None
        self.hovered_waypoint = None
        self.animation_data = self.animation_data_manager.animation_data        
        self.timelines = [Timeline(i) for i in range(len(self.animation_data.objects))]
        self.frame_control = FrameControl()
        self.event_handler = AnimationEditorEventHandler(self)
        

    def create_animation_data(self):        
        objects = [
            {"name": "Player", "imagePath": "player.png", "keyframes": []},
            {"name": "Enemy", "imagePath": "enemy.png", "keyframes": []}
        ]
        return AnimationData("ExampleAnimation", 2.0, 60, objects)



    def reset(self):
        pass

    def handle_events(self, event):
        self.event_handler.handle_events(event)


    def update_animation_data(self):
        self.animation_data_manager.update_animation_data(self.animation_data)


    def get_waypoint_position(self, waypoint_index):
        object_data = self.animation_data.objects[self.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if waypoint_index < len(keyframe_data):
            return keyframe_data[waypoint_index]["position"]
        else:
            return (0, 0)  # Default position if waypoint index is out of range

    def update_hovered_waypoint(self, pos):
        self.waypoint_manager.update_hovered_waypoint(pos)



    def update(self, dt):
        self.frame_control.update(dt)


    def draw(self):
        self.draw_background()
        self.draw_paths()
        self.draw_waypoints()
        self.draw_object_labels()
        self.draw_timelines()
        self.draw_frame_control()


    def draw_object_waypoints(self, object_index):
        object_data = self.animation_data.objects[object_index]
        keyframe_data = object_data["keyframes"]

        # Draw interpolated frames
        for frame in self.animation_data.interpolated_frames:
            if frame["frameNumber"] == self.frame_control.current_frame and frame["objectIndex"] == object_index:
                pygame.draw.circle(self.screen, settings.LIGHT_BLUE, frame["position"], 6)


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


    def draw_frame_control(self):
        self.frame_control.draw(self.screen)


    def draw_background(self):
        self.screen.fill(settings.BLACK)
        self.screen.blit(self.background, (0, 0))

    def draw_paths(self):
        for i in range(len(self.animation_data.objects)):
            self.draw_path(i)


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


    def save_animation_data(self):
        self.animation_data_manager.save_animation_data()


    def add_waypoint(self, pos):
        self.waypoint_manager.add_waypoint(pos)

    def delete_selected_waypoint(self):
        self.waypoint_manager.delete_selected_waypoint()


    def start_dragging_waypoint(self, pos):
        self.waypoint_manager.start_dragging_waypoint(pos)

    def stop_dragging_waypoint(self):
        self.waypoint_manager.stop_dragging_waypoint()

    def drag_waypoint(self, pos):
        self.waypoint_manager.drag_waypoint(pos)


    def draw_waypoints(self):
        for i in range(len(self.animation_data.objects)):
            self.draw_object_waypoints(i)


    def draw_path(self, object_index):
        object_data = self.animation_data.objects[object_index]
        keyframe_data = object_data["keyframes"]

        if len(keyframe_data) >= 2:
            color = settings.WHITE if object_index == self.selected_object else settings.GREY
            path = np.array([kf["position"] for kf in keyframe_data])
            smooth_path = create_smooth_path(path)
            pygame.draw.lines(self.screen, color, False, smooth_path, 2)
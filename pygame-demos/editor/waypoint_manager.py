import pygame
import numpy as np
from shared import game_settings as settings

class WaypointManager:
    def __init__(self, animation_editor):
        self.animation_editor = animation_editor

    def get_waypoint_position(self, waypoint_index):
        object_data = self.animation_editor.animation_data.objects[self.animation_editor.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if waypoint_index < len(keyframe_data):
            return keyframe_data[waypoint_index]["position"]
        else:
            return (0, 0)  # Default position if waypoint index is out of range

    def update_hovered_waypoint(self, pos):
        object_data = self.animation_editor.animation_data.objects[self.animation_editor.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if len(keyframe_data) > 0:
            positions = np.array([kf["position"] for kf in keyframe_data])
            pos_array = np.array(pos)
            distances = np.linalg.norm(positions - pos_array, axis=1)
            nearest_index = np.argmin(distances)

            if distances[nearest_index] <= 10:  # Adjust the threshold as needed
                self.animation_editor.hovered_waypoint = nearest_index
            else:
                self.animation_editor.hovered_waypoint = None
        else:
            self.animation_editor.hovered_waypoint = None

    def add_waypoint(self, pos):
        object_data = self.animation_editor.animation_data.objects[self.animation_editor.selected_object]
        keyframe_data = object_data["keyframes"]
        
        keyframe = {
            "frameNumber": self.animation_editor.frame_control.current_frame,
            "position": list(pos),
            "scale": [1, 1],
            "rotation": 0,
            "opacity": 1.0
        }
        keyframe_data.append(keyframe)
        keyframe_data.sort(key=lambda kf: kf["frameNumber"])

    def delete_selected_waypoint(self):
        object_data = self.animation_editor.animation_data.objects[self.animation_editor.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if self.animation_editor.hovered_waypoint is not None and self.animation_editor.hovered_waypoint < len(keyframe_data):
            del keyframe_data[self.animation_editor.hovered_waypoint]
            self.animation_editor.hovered_waypoint = None

    def start_dragging_waypoint(self, pos):
        object_data = self.animation_editor.animation_data.objects[self.animation_editor.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if len(keyframe_data) > 0:
            positions = np.array([kf["position"] for kf in keyframe_data])
            pos_array = np.array(pos)
            distances = np.linalg.norm(positions - pos_array, axis=1)
            nearest_index = np.argmin(distances)

            if distances[nearest_index] <= 10:  # Adjust the threshold as needed
                self.animation_editor.dragged_waypoint = nearest_index

    def stop_dragging_waypoint(self):
        self.animation_editor.dragged_waypoint = None

    def drag_waypoint(self, pos):
        object_data = self.animation_editor.animation_data.objects[self.animation_editor.selected_object]
        keyframe_data = object_data["keyframes"]
        
        if self.animation_editor.dragged_waypoint is not None and self.animation_editor.dragged_waypoint < len(keyframe_data):
            keyframe_data[self.animation_editor.dragged_waypoint]["position"] = list(pos)
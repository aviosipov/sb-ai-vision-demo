# editor/timeline.py
import pygame
from shared import game_settings as settings

class Timeline:
    def __init__(self, index):
        self.index = index
        self.num_frames = 60
        self.line_color = settings.WHITE
        self.keyframe_color = settings.GREEN

    def draw(self, screen, y_pos, current_frame, keyframes):
        container_width = settings.SCREEN_WIDTH - 40
        container_height = 10
        container_x = 20
        container_y = 10 + y_pos * 20

        pygame.draw.line(screen, self.line_color, (container_x, container_y), (container_x + container_width, container_y), 1)

        for keyframe in keyframes:
            keyframe_x = keyframe["frameNumber"] * container_width // self.num_frames + container_x
            pygame.draw.circle(screen, self.keyframe_color, (keyframe_x, container_y), 2)

        # Draw the current frame indicator
        current_frame_x = current_frame * container_width // self.num_frames + container_x
        pygame.draw.line(screen, settings.RED, (current_frame_x, container_y - 5), (current_frame_x, container_y + 5), 2)
# editor/timeline.py
import pygame
from shared import game_settings as settings

class Timeline:
    def __init__(self, index):
        self.index = index
        self.num_frames = 60
        self.dot_size = 4
        self.line_width = 2
        self.line_color = settings.WHITE
        self.dot_color = settings.GREY
        self.current_frame_color = settings.YELLOW

    def draw(self, screen, y_pos, current_frame):
        container_width = settings.SCREEN_WIDTH * 0.8
        container_height = 20
        container_x = (settings.SCREEN_WIDTH - container_width) // 2
        container_y = 50 + y_pos * 30

        pygame.draw.line(screen, self.line_color, (container_x, container_y), (container_x + container_width, container_y), self.line_width)

        dot_spacing = container_width / (self.num_frames - 1)
        for i in range(self.num_frames):
            dot_x = container_x + i * dot_spacing
            dot_color = self.current_frame_color if i + 1 == current_frame else self.dot_color
            pygame.draw.circle(screen, dot_color, (int(dot_x), container_y), self.dot_size)
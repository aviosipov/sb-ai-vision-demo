import pygame
from shared import game_settings as settings
from shared.font import load_font

class FrameControl:
    def __init__(self):
        self.current_frame = 1
        self.min_frame = 1
        self.max_frame = 60
        self.font_size = 24
        self.play_mode = False
        self.frame_change_delay = 0.1  # Adjust this value to control the frame change speed
        self.frame_change_timer = 0
        self.frame_change_direction = 0

    def increase_frame(self):
        self.current_frame = min(self.current_frame + 1, self.max_frame)

    def decrease_frame(self):
        self.current_frame = max(self.current_frame - 1, self.min_frame)

    def set_frame(self, frame):
        self.current_frame = max(min(frame, self.max_frame), self.min_frame)

    def toggle_play_mode(self):
        self.play_mode = not self.play_mode

    def start_frame_change(self, direction):
        self.frame_change_direction = direction

    def stop_frame_change(self):
        self.frame_change_direction = 0

    def update(self, dt):
        if self.play_mode:
            self.frame_change_timer += dt
            if self.frame_change_timer >= self.frame_change_delay:
                self.increase_frame()
                self.frame_change_timer = 0
                if self.current_frame == self.max_frame:
                    self.stop_frame_change()
        elif self.frame_change_direction != 0:
            self.frame_change_timer += dt
            if self.frame_change_timer >= self.frame_change_delay:
                if self.frame_change_direction > 0:
                    self.increase_frame()
                else:
                    self.decrease_frame()
                self.frame_change_timer = 0

    def draw(self, screen):
        font = load_font(self.font_size)
        text = font.render(str(self.current_frame), True, settings.WHITE)
        text_rect = text.get_rect(topright=(settings.SCREEN_WIDTH - 10, 10))
        screen.blit(text, text_rect)
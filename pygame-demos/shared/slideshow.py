import pygame
import math

class SlideshowConfig:
    def __init__(self, audio_file, image_files):
        self.audio_file = audio_file
        self.image_files = image_files
        self.breathing_duration = 1200
        self.zoom_speed = 0.05
        self.pan_speed = 0.02
        self.max_zoom_level = 1.8
        self.fade_out_duration = 2000

class Slideshow:
    def __init__(self, screen, config):
        self.screen = screen
        self.config = config
        self.audio_duration = 0
        self.image_duration = 0
        self.current_image_index = 0
        self.start_time = 0
        self.sequence_played = False
        self.fade_out_alpha = 255
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.target_pan_x = 0
        self.target_pan_y = 0

        self.load_assets()


    def load_assets(self):
        pygame.mixer.music.load(self.config.audio_file)
        self.audio_duration = pygame.mixer.Sound(self.config.audio_file).get_length() * 1000  # Convert to milliseconds
        
        self.images = [self.scale_image(image_file) for image_file in self.config.image_files]
        self.image_duration = self.audio_duration // len(self.images)

    def scale_image(self, image_file):
        image = pygame.image.load(image_file)
        aspect_ratio = image.get_width() / image.get_height()
        
        if aspect_ratio > self.screen.get_width() / self.screen.get_height():
            new_width = self.screen.get_width()
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = self.screen.get_height()
            new_width = int(new_height * aspect_ratio)
        
        return pygame.transform.scale(image, (new_width, new_height))

    def smooth_value(self, start, end, t):
        t = min(max(t, 0.0), 1.0)  # Clamp t between 0 and 1
        t = (1 - math.cos(t * math.pi)) / 2  # Smooth the value using a cosine function
        return start * (1 - t) + end * t

    def update(self, dt):
        if not self.sequence_played:
            self.start_time = pygame.time.get_ticks()
            pygame.mixer.music.play()
            self.sequence_played = True
            self.reset_zoom_pan()

        if self.sequence_played:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            self.current_image_index = min(int(elapsed_time // self.image_duration), len(self.images) - 1)

            if self.current_image_index < len(self.images) - 1:
                self.update_zoom_pan(dt)
            else:
                self.zoom_level = min(self.zoom_level + self.config.zoom_speed * dt, self.config.max_zoom_level)
                self.pan_x = self.smooth_value(self.pan_x, self.target_pan_x, self.config.pan_speed)
                self.pan_y = self.smooth_value(self.pan_y, self.target_pan_y, self.config.pan_speed)

            if not pygame.mixer.music.get_busy():
                self.fade_out_alpha = max(self.fade_out_alpha - int(255 * dt / (self.config.fade_out_duration / 1000)), 0)

    def reset_zoom_pan(self):
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.target_pan_x = 0
        self.target_pan_y = 0

    def set_target_pan(self):
        self.target_pan_x = (self.current_image_index % 2) * 100 - 50  # Alternate between -50 and 50
        self.target_pan_y = (self.current_image_index % 2) * 60 - 30  # Alternate between -30 and 30

    def update_zoom_pan(self, dt):
        self.zoom_level = min(self.zoom_level + self.config.zoom_speed * dt, self.config.max_zoom_level)
        self.pan_x = self.smooth_value(self.pan_x, self.target_pan_x, self.config.pan_speed)
        self.pan_y = self.smooth_value(self.pan_y, self.target_pan_y, self.config.pan_speed)

    def draw(self):
        if 0 <= self.current_image_index < len(self.images):
            image = self.images[self.current_image_index]
            image_rect = image.get_rect()
            image_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

            scaled_width = int(image_rect.width * self.zoom_level)
            scaled_height = int(image_rect.height * self.zoom_level)
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))
            scaled_rect = scaled_image.get_rect()
            scaled_rect.center = (self.screen.get_width() // 2 + self.pan_x, self.screen.get_height() // 2 + self.pan_y)

            image_copy = scaled_image.copy()
            image_copy.set_alpha(self.fade_out_alpha)
            self.screen.blit(image_copy, scaled_rect)
            
    def reset(self):
        self.current_image_index = 0
        self.start_time = 0
        self.sequence_played = False
        self.fade_out_alpha = 255
        self.reset_zoom_pan()
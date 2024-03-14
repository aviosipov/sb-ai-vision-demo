import pygame
from shared import game_settings as settings
import math
from shared.scene import Scene

class GameOverConfig:
    def __init__(self):
        self.fade_out_duration = 1000  # Fade out duration in milliseconds
        self.breathing_duration = 1000  # Breathing effect duration in milliseconds
        self.zoom_speed = 0.05
        self.pan_speed = 0.02
        self.max_zoom_level = 1.8

class GameOver(Scene):
    def __init__(self, screen, audio_file, image_files, config):
        super().__init__(screen)  # Call the parent class constructor
        self.screen = screen
        self.audio_file = audio_file
        self.image_files = image_files
        self.config = config
        self.audio_duration = 0
        self.image_duration = 0
        self.current_image_index = 0
        self.start_time = 0
        self.sequence_played = False
        self.fade_out_alpha = 255
        self.breathing_timer = 0
        self.text_alpha = 255
        self.zoom_level = 1.0
        self.pan_x = 0
        self.pan_y = 0
        self.target_pan_x = 0
        self.target_pan_y = 0

        self.load_assets()





    def load_assets(self):
        pygame.mixer.music.load(self.audio_file)
        self.audio_duration = pygame.mixer.Sound(self.audio_file).get_length() * 1000  # Convert to milliseconds
        
        self.images = [self.scale_image(image_file) for image_file in self.image_files]
        self.image_duration = self.audio_duration // len(self.images)

    def scale_image(self, image_file):
        image = pygame.image.load(image_file)
        aspect_ratio = image.get_width() / image.get_height()
        
        if aspect_ratio > settings.SCREEN_WIDTH / settings.SCREEN_HEIGHT:
            new_width = settings.SCREEN_WIDTH
            new_height = int(new_width / aspect_ratio)
        else:
            new_height = settings.SCREEN_HEIGHT
            new_width = int(new_height * aspect_ratio)
        
        return pygame.transform.scale(image, (new_width, new_height))

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            pygame.mixer.music.stop()
            self.next_scene = "start_game"  # Set the next_scene attribute to "start_game"



    def smooth_value(self, start, end, t):
        t = min(max(t, 0.0), 1.0)  # Clamp t between 0 and 1
        t = (1 - math.cos(t * math.pi)) / 2  # Smooth the value using a cosine function
        return start * (1 - t) + end * t

    def update(self, dt):
        if not pygame.mixer.music.get_busy() and not self.sequence_played:
            self.start_time = pygame.time.get_ticks()
            pygame.mixer.music.play()
            self.sequence_played = True
            self.reset_zoom_pan()

        if self.sequence_played:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            prev_image_index = self.current_image_index
            self.current_image_index = int(min(elapsed_time // self.image_duration, len(self.images) - 1))

            if self.current_image_index != prev_image_index:
                self.reset_zoom_pan()
                self.set_target_pan()

            if elapsed_time >= self.audio_duration:
                pygame.mixer.music.stop()
                self.fade_out_alpha = max(self.fade_out_alpha - int(255 * dt / (self.config.fade_out_duration / 1000)), 0)

            self.update_zoom_pan(dt)

        self.breathing_timer = (self.breathing_timer + dt * 1000) % self.config.breathing_duration
        self.text_alpha = int(255 * (1 - (self.breathing_timer / self.config.breathing_duration)))

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
        if self.current_image_index >= 0:
            image = self.images[self.current_image_index]
            image_rect = image.get_rect()
            image_rect.center = (settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2)

            scaled_width = int(image_rect.width * self.zoom_level)
            scaled_height = int(image_rect.height * self.zoom_level)
            scaled_image = pygame.transform.scale(image, (scaled_width, scaled_height))
            scaled_rect = scaled_image.get_rect()
            scaled_rect.center = (settings.SCREEN_WIDTH // 2 + self.pan_x, settings.SCREEN_HEIGHT // 2 + self.pan_y)

            image_copy = scaled_image.copy()
            image_copy.set_alpha(self.fade_out_alpha)
            self.screen.blit(image_copy, scaled_rect)
        else:
            self.screen.fill(settings.BLACK)

        
        self.draw_text("press enter to try again", settings.WHITE, (settings.SCREEN_WIDTH // 2 , settings.SCREEN_HEIGHT - 50), self.text_alpha)
        

    def draw_text(self, text, color, center, alpha=255):
        font = pygame.font.SysFont(None, 24)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=center)
        text_surface.set_alpha(alpha)
        self.screen.blit(text_surface, text_rect)

    def reset(self):
        pygame.mixer.music.stop()
        self.current_image_index = 0
        self.start_time = 0
        self.sequence_played = False
        self.fade_out_alpha = 255
        self.breathing_timer = 0
        self.text_alpha = 255
        self.reset_zoom_pan()
        self.next_scene = None  # Reset the next_scene attribute

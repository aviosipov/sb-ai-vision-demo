import pygame
import math

class SlideshowConfig:
    def __init__(self, audio_file, slides):
        self.audio_file = audio_file
        self.slides = slides
        self.breathing_duration = 1200
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
        
        self.slides = []
        for slide_config in self.config.slides:
            image = self.scale_image(slide_config["image"])
            text = slide_config["text"]
            time = slide_config["time"]
            self.slides.append({"image": image, "text": text, "time": time})

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


    def update(self, dt):
        if not self.sequence_played:
            self.start_time = pygame.time.get_ticks()
            pygame.mixer.music.load(self.config.audio_file)
            pygame.mixer.music.play()
            self.sequence_played = True

        if self.sequence_played:
            elapsed_time = pygame.time.get_ticks() - self.start_time
            self.current_slide_index = None
            for i, slide in enumerate(self.slides):
                if elapsed_time >= slide["time"] * 1000:
                    self.current_slide_index = i
                else:
                    break

            if not pygame.mixer.music.get_busy():
                self.fade_out_alpha = max(self.fade_out_alpha - int(255 * dt / (self.config.fade_out_duration / 1000)), 0)
                if self.fade_out_alpha == 0:
                    self.sequence_played = False


    def draw(self):
        if self.current_slide_index is not None:
            slide = self.slides[self.current_slide_index]
            image = slide["image"]
            text = slide["text"]
            
            image_rect = image.get_rect()
            image_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)

            image_copy = image.copy()
            image_copy.set_alpha(self.fade_out_alpha)
            self.screen.blit(image_copy, image_rect)

            font = pygame.font.Font(None, 36)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect()
            text_rect.centerx = self.screen.get_width() // 2
            text_rect.top = image_rect.bottom + 20
            text_surface.set_alpha(self.fade_out_alpha)
            self.screen.blit(text_surface, text_rect)


                
    def reset(self):
        self.current_slide_index = 0
        self.start_time = 0
        self.sequence_played = False
        self.fade_out_alpha = 255
        pygame.mixer.music.stop()

import pygame
import math
from shared.font import load_font

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
        self.start_time = 0
        self.sequence_played = False
        self.fade_out_alpha = 255
        self.current_slide_index = 0
        self.zoom_level = 1.0
        self.zoom_factor = 0.05
        self.font_size = 36
        self.text_spacing = 20

        self.font_size = 36
        self.text_spacing = 20
        self.max_text_height = 200
        self.text_color = (255, 255, 255)


        self.load_assets()

    def load_assets(self):
        pygame.mixer.music.load(self.config.audio_file)
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
            self.start_sequence()

        if self.sequence_played:
            self.update_current_slide()
            self.update_zoom(dt)
            self.update_fade_out(dt)

    def start_sequence(self):
        self.start_time = pygame.time.get_ticks()
        pygame.mixer.music.load(self.config.audio_file)
        pygame.mixer.music.play()
        self.sequence_played = True

    def update_current_slide(self):
        elapsed_time = pygame.time.get_ticks() - self.start_time
        self.current_slide_index = None
        for i, slide in enumerate(self.slides):
            if elapsed_time >= slide["time"] * 1000:
                self.current_slide_index = i
            else:
                break

    def update_zoom(self, dt):
        if self.current_slide_index is not None:
            self.zoom_level += self.zoom_factor * dt

    def update_fade_out(self, dt):
        if not pygame.mixer.music.get_busy():
            self.fade_out_alpha = max(self.fade_out_alpha - int(255 * dt / (self.config.fade_out_duration / 1000)), 0)
            if self.fade_out_alpha == 0:
                self.sequence_played = False

    def draw(self):
        if self.current_slide_index is not None:
            slide = self.slides[self.current_slide_index]
            self.draw_image(slide["image"])
            self.draw_text(slide["text"], 20, 120, 12)

    def draw_image(self, image):
        scaled_image_width = int(image.get_width() * self.zoom_level)
        scaled_image_height = int(image.get_height() * self.zoom_level)
        scaled_image = pygame.transform.smoothscale(image, (scaled_image_width, scaled_image_height))
        image_rect = scaled_image.get_rect()
        image_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2)
        image_copy = scaled_image.copy()
        image_copy.set_alpha(self.fade_out_alpha)
        self.screen.blit(image_copy, image_rect)



    def draw_text(self, text, size = 16, y_pos = 80 , text_spacing = 12):
        font = load_font(size)
        text_lines = self.wrap_text(text, font, self.screen.get_width() - text_spacing * 2.5)

        text_height = min(len(text_lines) * (font.get_height() + 5), self.max_text_height)
        text_rect = pygame.Rect(0, 0, self.screen.get_width(), text_height)
        text_rect.centerx = self.screen.get_width() // 2
        text_rect.top = y_pos

        for i, line in enumerate(text_lines):
            text_surface = font.render(line, True, self.text_color)
            text_line_rect = text_surface.get_rect()
            text_line_rect.centerx = text_rect.centerx
            text_line_rect.top = text_rect.top + i * (font.get_height() + 5)
            text_surface.set_alpha(self.fade_out_alpha)
            self.screen.blit(text_surface, text_line_rect)


    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + " " + word if current_line else word
            test_width = font.size(test_line)[0]

            if test_width <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    def reset(self):
        self.current_slide_index = 0
        self.start_time = 0
        self.zoom_level = 1.0
        self.sequence_played = False
        self.fade_out_alpha = 255
        pygame.mixer.music.stop()
# scene.py
import pygame

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None
        self.bg_music = None  # Add this line

    def play_bg_music(self, loops=-1):
        if self.bg_music:
            pygame.mixer.music.stop()
            pygame.mixer.music.load(self.bg_music)
            pygame.mixer.music.play(loops)


    def stop_bg_music(self):
        pygame.mixer.music.stop()


    def handle_events(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass

    def reset(self):
        pass

    def switch_to_scene(self, next_scene):
        self.stop_bg_music()
        self.next_scene = next_scene

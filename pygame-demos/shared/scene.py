# scene.py
import pygame

class Scene:
    def __init__(self, screen):
        self.screen = screen
        self.next_scene = None

    def handle_events(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self):
        pass

    def reset(self):
        pass

    def switch_to_scene(self, next_scene):
        self.next_scene = next_scene
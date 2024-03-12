# bullet.py
import pygame
from shared.game_object import GameObject

class Bullet(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 4, 160)
        self.color = (225, 225, 225)  # White

    def move(self, dt):
        self.y -= self.speed * dt

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)
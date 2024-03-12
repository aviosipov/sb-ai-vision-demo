# game_object.py
import uuid
from shared import game_settings as settings

class GameObject:
    def __init__(self, x, y, size, speed, name=None):
        self.x = x
        self.y = y
        self.size = size
        self.speed = speed
        self.to_remove = False
        self.name = name or self.generate_name()

    def generate_name(self):
        return f"{self.__class__.__name__.lower()}_{uuid.uuid4().hex[:6]}"

    def update(self, dt):
        self.move(dt)

    def move(self, dt):
        pass

    def draw(self, screen):
        pass

    def is_off_screen(self):
        return self.y < 0 or self.y > settings.SCREEN_HEIGHT

    def remove(self):
        self.to_remove = True

    def collides_with(self, other):
        return (
            self.x < other.x + other.size and
            self.x + self.size > other.x and
            self.y < other.y + other.size and
            self.y + self.size > other.y
        )
# npc.py
import pygame
import random
from shared import game_settings as settings
from shared.bullet import Bullet
from shared.game_object import GameObject
from shared.game_state import game_state

class NPC(GameObject):
    def __init__(self, screen):

        self.move_direction = 1  # 1 for right, -1 for left
        self.move_interval = random.randint(30, 90)  # Random interval for changing direction
        self.move_timer = 0
        self.speed = 25.0  # Adjust this value to control the speed


        self.screen = screen
        self.size = 48
        self.speed = 155.1
        self.color = (255, 127, 120)  # Coral
        self.hit_tint_duration = 4
        self.hit_tint_color = (255, 0, 0)  # Red
        self.hit_tint_timer = 0
        
        

        self.original_image = pygame.image.load('assets/enemy.png')
        self.image = pygame.transform.scale(self.original_image, (self.size, self.size))
        super().__init__(0, 0, self.size, self.speed)
        self.reset()

        selected_spaceship = game_state.get_selected_spaceship()
        self.health = 10 * selected_spaceship['damage']
        

        

    def reset(self):
        self.x = random.randint(0, settings.SCREEN_WIDTH - self.size)
        self.y = 0
        self.hit_tint_timer = 0
        self.move_direction = random.choice([-1, 1])  # Randomly choose the initial direction
        self.move_timer = 0
        self.move_interval = random.randint(30, 90)  # Set a new random interval


    def move(self, dt):
        self.y += self.speed * dt
        self.x += self.move_direction * self.speed * dt

        self.move_timer += 1
        if self.move_timer >= self.move_interval:
            self.move_direction *= -1  # Change direction
            self.move_timer = 0
            self.move_interval = random.randint(30, 90)  # Set a new random interval

        # Keep the NPC within the screen bounds
        if self.x <= 0:
            self.x = 0
            self.move_direction = 1
        elif self.x >= settings.SCREEN_WIDTH - self.size:
            self.x = settings.SCREEN_WIDTH - self.size
            self.move_direction = -1

        if self.is_off_screen():
            self.remove()


    def update(self, dt):
        self.move(dt)
        if self.hit_tint_timer > 0:
            self.hit_tint_timer -= 1
            if self.hit_tint_timer <= 0:
                self.remove()  # Check for removal after hit tint timer expires

    def draw(self):
        if self.hit_tint_timer > 0:
            tinted_image = self.image.copy()
            tinted_image.fill(self.hit_tint_color, special_flags=pygame.BLEND_RGB_MULT)
            self.screen.blit(tinted_image, (int(self.x), int(self.y)))
        else:
            self.screen.blit(self.image, (int(self.x), int(self.y)))

    def on_collision(self, target):
        if isinstance(target, Bullet):
            self.start_hit_tint()
            target.remove()
            # Check if the hit tint timer has expired before removing the NPC
            if self.hit_tint_timer <= 0:
                self.remove()

    def start_hit_tint(self):
        self.hit_tint_timer = self.hit_tint_duration
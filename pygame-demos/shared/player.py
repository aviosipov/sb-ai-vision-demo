import pygame
from shared import game_settings as settings
import math
from shared.npc import NPC
from shared.bullet import Bullet

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 90
PADDLE_SPEED = 185

class Player:
    def __init__(self, screen, offset_x=0, offset_y=0):
        self.screen = screen
        self.original_image = pygame.image.load('assets/player.png')
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.x = settings.SCREEN_WIDTH // 2 - self.width // 2
        self.y = settings.SCREEN_HEIGHT - self.height - offset_y
        self.bullets = []
        self.health = 100
        self.moving_left = False
        self.moving_right = False
        # Hit tint attributes
        self.hit_tint_duration = 3
        self.hit_tint_timer = 0
        self.hit_tint_color = (255, 0, 0)  # Red for hit tint

    def reset(self):
        self.x = settings.SCREEN_WIDTH // 2 - self.width // 2
        self.y = settings.SCREEN_HEIGHT - self.height - 20  # Adjust the offset as needed
        self.bullets = []
        self.moving_left = False
        self.moving_right = False
        self.hit_tint_timer = 0



    def shoot(self):
        bullet_x = self.x + self.width // 2
        bullet_y = self.y
        bullet = Bullet(bullet_x, bullet_y)
        self.bullets.append(bullet)

    def update(self, dt):
        if self.moving_left:
            self.move_left(dt)
        elif self.moving_right:
            self.move_right(dt)

        for bullet in self.bullets:
            bullet.update(dt)
            if bullet.is_off_screen() or bullet.to_remove:
                self.bullets.remove(bullet)

        self.bullets = [bullet for bullet in self.bullets if not bullet.is_off_screen()]

        if self.hit_tint_timer > 0:
            self.hit_tint_timer -= 1


    def move_left(self, dt):
        self.x = max(0, self.x - PADDLE_SPEED * dt)

    def move_right(self, dt):
        self.x = min(settings.SCREEN_WIDTH - self.width, self.x + PADDLE_SPEED * dt)

    def draw(self):
        # Apply tint if hit_tint_timer is active
        if self.hit_tint_timer > 0:
            tinted_image = self.image.copy()
            tinted_image.fill(self.hit_tint_color, special_flags=pygame.BLEND_RGB_MULT)
            self.screen.blit(tinted_image, (self.x, self.y))
        else:
            self.screen.blit(self.image, (self.x, self.y))
        # Drawing bullets...
        for bullet in self.bullets:
            bullet.draw(self.screen)

    def collides_with(self, shape):
        return self.y < shape.y + shape.size and shape.x < self.x + self.width and shape.x + shape.size > self.x

    def on_collision(self, target):
        # Collision handling, including starting the hit tint timer
        if isinstance(target, NPC):
            self.take_damage(20)
            self.hit_tint_timer = self.hit_tint_duration  # Start hit tint

    def on_miss(self):
        # Method implementation remains the same...
        self.take_damage(10)
        self.hit_tint_timer = self.hit_tint_duration  # Start hit tint on miss as well


    def take_damage(self, amount):
        # Damage taking logic...
        self.health -= amount
        # Start the hit tint timer whenever damage is taken
        self.hit_tint_timer = self.hit_tint_duration

    def is_alive(self):
        return self.health > 0
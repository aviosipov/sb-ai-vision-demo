import pygame
from shared import game_settings as settings
import math
from shared.npc import NPC
from shared.bullet import Bullet
from shared.game_state import game_state

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 90


class Player:
    def __init__(self, screen, selected_spaceship, offset_x=0, offset_y=0):
        self.screen = screen
        self.original_image = pygame.image.load(selected_spaceship['image'])
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
        self.last_shot_time = 0
        self.hit_tint_timer = 0
        self.hit_tint_color = (255, 0, 0)  # Red for hit tint

        self.speed = selected_spaceship['speed']      
        self.reload_rate = selected_spaceship['reload_rate']


    def reset(self, selected_spaceship):
        self.original_image = pygame.image.load(selected_spaceship['image'])
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.image = pygame.transform.scale(self.original_image, (self.width, self.height))
        self.x = settings.SCREEN_WIDTH // 2 - self.width // 2
        self.y = settings.SCREEN_HEIGHT - self.height - 20  # Adjust the offset as needed
        self.bullets = []
        self.moving_left = False
        self.moving_right = False
        self.hit_tint_timer = 0
        self.speed = selected_spaceship['speed']        
        self.reload_rate = selected_spaceship['reload_rate']

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if pygame.key.get_pressed()[pygame.K_SPACE] and current_time - self.last_shot_time >= self.reload_rate * 1000:
            bullet_x = self.x + self.width // 2
            bullet_y = self.y
            bullet = Bullet(bullet_x, bullet_y)
            self.bullets.append(bullet)
            self.last_shot_time = current_time

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
        self.x = max(0, self.x - self.speed * dt)

    def move_right(self, dt):
        self.x = min(settings.SCREEN_WIDTH - self.width, self.x + self.speed * dt)

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
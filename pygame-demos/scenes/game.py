import pygame
from shared import game_settings as settings
from shared.grid import draw_grid
from shared.player import Player
from shared.npc import NPC
from shared.scene import Scene

class Game(Scene):
    def __init__(self, screen):
        super().__init__(screen)  # Call the parent class constructor
        self.screen = screen
        self.player = Player(self.screen, offset_y=20)
        self.score = 0
        self.game_over = False
        self.npc_spawn_interval = 1250
        self.npc_last_spawn_time = 0
        self.max_npcs = 6
        self.npcs = []
        self.background_image = pygame.image.load('assets/game-bg.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def reset(self):
        self.player.reset()
        self.player.health = 100  # Reset the player's health
        self.score = 0
        self.game_over = False
        self.npc_last_spawn_time = 0
        self.npcs = []
        self.next_scene = None  # Reset the next_scene attribute

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.player.moving_right = True
            elif event.key == pygame.K_g:
                settings.SHOW_GRID = not settings.SHOW_GRID
            elif event.key == pygame.K_SPACE:
                self.player.shoot()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.player.moving_right = False

    def update(self, dt):
        self.player.update(dt)
        self.update_npcs(dt)
        self.spawn_npcs()
        self.check_collisions()

        if not self.player.is_alive():
            self.game_over = True
            self.switch_to_scene("game_over")  # Use the switch_to_scene method





    def update_npcs(self, dt):
        for npc in self.npcs:
            npc.update(dt)
            if npc.is_off_screen() or npc.to_remove:
                self.npcs.remove(npc)

    def spawn_npcs(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.npc_last_spawn_time >= self.npc_spawn_interval and len(self.npcs) < self.max_npcs:
            npc = NPC(self.screen)
            self.npcs.append(npc)
            self.npc_last_spawn_time = current_time

    def check_collisions(self):
        for bullet in self.player.bullets:
            for npc in self.npcs:
                if npc.collides_with(bullet):
                    self.score += 10
                    npc.on_collision(bullet)
                    break
        
        for npc in self.npcs:
            if self.player.collides_with(npc):
                self.player.on_collision(npc)
                npc.remove()
            
            if npc.y + npc.size > settings.SCREEN_HEIGHT:  # Check if NPC hits the ground
                self.player.on_miss()
                npc.reset()


    def draw(self):
        self.screen.blit(self.background, (0, 0))

        if settings.SHOW_GRID:
            draw_grid(self.screen)

        self.player.draw()

        for npc in self.npcs:
            npc.draw()

        self.draw_score_and_health()


    def draw_score_and_health(self):
        font = pygame.font.SysFont(None, 25)
        score_text = font.render("Score: " + str(self.score), True, settings.WHITE)
        self.screen.blit(score_text, (10, 10))

        health_text = font.render("Health: " + str(self.player.health), True, settings.WHITE)
        self.screen.blit(health_text, (10, 30))
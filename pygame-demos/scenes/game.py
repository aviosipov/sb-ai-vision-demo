# scenes/game.py
import pygame
from shared import game_settings as settings
from shared.grid import draw_grid
from shared.player import Player
from shared.npc import NPC
from shared.scene import Scene
from shared.font import load_font
from shared.ui import draw_info_box
from shared.game_state import game_state
import random
from shared.scene_utils import handle_scene_restart

class Game(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.bg_music = "assets/audio/bg1.mp3"  # Set the background music file
        self.countdown_timer = 3000  # Countdown duration in milliseconds
        self.game_started = False

        selected_spaceship = game_state.get_selected_spaceship()
        if selected_spaceship is None:
            # Set a default spaceship if none is selected
            selected_spaceship = {
                "image": "assets/spaceships/spaceship1.png",
                "damage": 10,
                "speed": 5,
                "reload_rate": 1,
                "health": 100  # Add the 'health' key with an appropriate value
            }

        self.player = Player(self.screen, selected_spaceship, offset_y=20)
        self.score = 0
        self.game_over = False
        self.npc_spawn_interval = 5000
        self.npc_last_spawn_time = 0
        self.max_npcs = 5  # Increase the maximum number of NPCs to 5
        self.npcs = []
        self.background_image = pygame.image.load('assets/game-bg.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def reset(self):
        selected_spaceship = game_state.get_selected_spaceship()
        if selected_spaceship is None:
            # Set a default spaceship if none is selected
            selected_spaceship = {
                "image": "assets/spaceships/spaceship1.png",
                "damage": 10,
                "speed": 5,
                "reload_rate": 1,
                "health": 100
            }
        self.player.reset(selected_spaceship)
        self.player.health = selected_spaceship['health']
        self.score = 0
        self.game_over = False
        self.npc_last_spawn_time = 0
        self.npcs = []
        self.next_scene = None
        self.play_bg_music()
        self.game_started = False  # Reset the game_started flag
        self.countdown_timer = 3000  # Reset the countdown timer


    def handle_events(self, event):
        handle_scene_restart(event, self.reset)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.player.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.player.moving_right = True
            elif event.key == pygame.K_g:
                settings.SHOW_GRID = not settings.SHOW_GRID
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.player.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.player.moving_right = False


    def update(self, dt):
        if not self.game_started:
            self.countdown_timer -= dt * 1000
            if self.countdown_timer <= 0:
                self.game_started = True
        else:
            self.player.update(dt)
            self.player.shoot()

            self.update_npcs(dt)
            self.spawn_npcs()
            self.check_collisions()

            if not self.player.is_alive():
                self.game_over = True
                self.switch_to_scene("game_over")

    def draw_countdown(self):
        countdown_text = ""
        if self.countdown_timer > 2000:
            countdown_text = "3"
        elif self.countdown_timer > 1000:
            countdown_text = "2"
        elif self.countdown_timer > 0:
            countdown_text = "1"
        else:
            countdown_text = "GO!"

        font = load_font(72)
        text_surface = font.render(countdown_text, True, settings.WHITE)
        text_rect = text_surface.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT // 2))
        self.screen.blit(text_surface, text_rect)

    def update_npcs(self, dt):
        for npc in self.npcs:
            npc.update(dt)
            if npc.is_off_screen() or npc.to_remove:
                self.npcs.remove(npc)

    def spawn_npcs(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.npc_last_spawn_time >= self.npc_spawn_interval and len(self.npcs) < self.max_npcs:
            for _ in range(self.max_npcs - len(self.npcs)):  # Spawn multiple NPCs at once
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

        if not self.game_started:
            self.draw_countdown()
        else:
            self.player.draw()

            for npc in self.npcs:
                npc.draw()

            self.draw_score_and_health()

    def draw_score_and_health(self):
        draw_info_box(self.screen, "Score", self.score, 15, 20, 95)
        draw_info_box(self.screen, "Health", self.player.health, 15, 50, 95)
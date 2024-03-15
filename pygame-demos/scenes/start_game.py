import pygame
from shared import game_settings as settings
from shared.scene import Scene
from shared.font import load_font

class StartGame(Scene):
    def __init__(self, screen):
        super().__init__(screen)
        self.screen = screen
        self.background_image = pygame.image.load('assets/start_game/game-intro.png')
        self.background = pygame.transform.scale(self.background_image, (settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))

    def reset(self):
        pass

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.next_scene = "spaceship_selection"  # Set the next_scene attribute to "spaceship_selection"
        return None

    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(settings.BLACK)
        font = load_font(22)
        text = font.render("Press Enter to Start", True, settings.WHITE)
        text_rect = text.get_rect(center=(settings.SCREEN_WIDTH // 2, settings.SCREEN_HEIGHT - 50))

        self.screen.blit(self.background, (0, 0))
        self.screen.blit(text, text_rect)

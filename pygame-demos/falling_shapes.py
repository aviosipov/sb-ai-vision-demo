import pygame
from shared import game_settings as settings
from scenes.start_game import StartGame
from scenes.game import Game
from scenes.game_over import GameOver, GameOverConfig

class FallingShapes:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        # Initialize GameOverConfig
        game_over_config = GameOverConfig()

        # Provide the required arguments for GameOver
        audio_file = "assets/game_over/story.mp3"
        image_files = ["assets/game_over/story1.png", "assets/game_over/story2.png", "assets/game_over/story3.png"]

        self.scenes = {
            "start_game": StartGame(self.screen),
            "game": Game(self.screen),
            "game_over": GameOver(self.screen, audio_file, image_files, game_over_config)
        }

        self.current_scene = "start_game"

    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                next_scene = self.scenes[self.current_scene].handle_events(event)
                if next_scene:
                    self.scenes[self.current_scene].reset()  # Reset the current scene
                    self.current_scene = next_scene

            next_scene = self.scenes[self.current_scene].update(dt)
            if next_scene:
                self.scenes[self.current_scene].reset()  # Reset the current scene
                self.current_scene = next_scene

            self.scenes[self.current_scene].draw()

            pygame.display.flip()

        pygame.quit()



if __name__ == "__main__":
    game = FallingShapes()
    game.run()

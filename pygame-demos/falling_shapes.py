import pygame
from shared import game_settings as settings
from scenes.start_game import StartGame
from scenes.game import Game
from scenes.game_over import GameOver
from scenes.spaceship_selection import SpaceshipSelection
from shared.game_state import game_state
from shared.slideshow import SlideshowConfig
from editor.animation_editor import AnimationEditor

class FallingShapes:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        audio_file = "assets/game_over/story.mp3"

        slides = [
            {"image": "assets/game_over/story1.png", "text": "In the final stand, our hero battles the alien force amidst the ruins of the city.", "time" : 0},
            {"image": "assets/game_over/story2.png", "text": "As our defenses fall, the relentless invasion darkens all hope. The city, once vibrant, now lies in shadows, a testament to our defeat.", "time": 7},
            {"image": "assets/game_over/story3.png", "text": "Yet, amidst the ruins, a spark of resistance flickers, promising that not all is lost.", "time": 14}
        ]

        slideshow_config = SlideshowConfig(audio_file, slides)

        self.scenes = {
            "start_game": StartGame(self.screen),
            "spaceship_selection": SpaceshipSelection(self.screen),
            "game": Game(self.screen),
            "game_over": GameOver(self.screen, slideshow_config),
            "animation_editor": AnimationEditor(self.screen)
        }

        self.current_scene = "start_game"


    def run(self):
        running = True
        while running:
            dt = self.clock.tick(60) / 1000

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.scenes[self.current_scene].handle_events(event)

            self.scenes[self.current_scene].update(dt)
            if self.scenes[self.current_scene].next_scene:
                if self.current_scene == "spaceship_selection" and self.scenes[self.current_scene].next_scene == "game":
                    self.scenes["game"] = Game(self.screen)  # Create the game scene
                elif self.current_scene == "game_over" and self.scenes[self.current_scene].next_scene == "start_game":
                    game_state.set_selected_spaceship(None)  # Reset the selected spaceship
                self.current_scene = self.scenes[self.current_scene].next_scene
                self.scenes[self.current_scene].reset()
                
                # Reset the next_scene attribute of the previous scene
                for scene_name, scene in self.scenes.items():
                    if scene_name != self.current_scene:
                        scene.next_scene = None

            self.scenes[self.current_scene].draw()

            pygame.display.flip()

        pygame.quit()


if __name__ == "__main__":
    game = FallingShapes()
    game.run()
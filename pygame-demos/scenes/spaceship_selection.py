import pygame
from shared import game_settings as settings
from shared.scene import Scene
from shared.font import load_font
from shared.game_state import game_state
from shared.ui import draw_info_box
from shared.scene_utils import handle_scene_restart

class SpaceshipSelection(Scene):
    def __init__(self, screen):
        super().__init__(screen)  # Call the parent class constructor
        self.screen = screen
        self.spaceships = [
            {"image": "assets/spaceships/spaceship1.png", "name": "Sparrow", "damage": 10, "speed": 50, "reload_rate": 1, "health": 100},
            {"image": "assets/spaceships/spaceship2.png", "name": "Phoenix", "damage": 15, "speed": 80, "reload_rate": 0.8, "health": 120},
            {"image": "assets/spaceships/spaceship3.png", "name": "Falcon", "damage": 12, "speed": 150, "reload_rate": 1.2, "health": 80},
            {"image": "assets/spaceships/spaceship4.png", "name": "Eagle", "damage": 4, "speed": 250, "reload_rate": 0.3, "health": 150}
        ]
        self.selected_spaceship = 0
        self.load_images()



    def load_images(self):
        self.spaceship_images = [pygame.image.load(spaceship["image"]) for spaceship in self.spaceships]
        self.scaled_images = []
        for image in self.spaceship_images:
            aspect_ratio = image.get_height() / image.get_width()
            new_width = int(settings.SCREEN_WIDTH * 0.7)
            new_height = int(new_width * aspect_ratio)
            scaled_image = pygame.transform.scale(image, (new_width, new_height))
            self.scaled_images.append(scaled_image)

    def reset(self):
        self.selected_spaceship = 0  # Reset the selected spaceship to the first one
        self.next_scene = None  # Reset the next_scene attribute

    def handle_events(self, event):
        handle_scene_restart(event, self.reset)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_spaceship = (self.selected_spaceship - 1) % len(self.spaceships)
            elif event.key == pygame.K_RIGHT:
                self.selected_spaceship = (self.selected_spaceship + 1) % len(self.spaceships)
            elif event.key == pygame.K_RETURN:
                selected_spaceship = self.spaceships[self.selected_spaceship]
                game_state.set_selected_spaceship(selected_spaceship)
                self.switch_to_scene("game")




    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(settings.BLACK)
        
        title_font = load_font(24)
        title_text = title_font.render("Select Your Ship", True, settings.WHITE)
        title_rect = title_text.get_rect(centerx=settings.SCREEN_WIDTH // 2, y=30)
        self.screen.blit(title_text, title_rect)
        
        current_image = self.scaled_images[self.selected_spaceship]
        x = settings.SCREEN_WIDTH // 2 - current_image.get_width() // 2
        y = 80
        self.screen.blit(current_image, (x, y))

        info_x = settings.SCREEN_WIDTH // 2 - 150
        info_y = settings.SCREEN_HEIGHT // 2

        name_font = load_font(18)
        current_spaceship = self.spaceships[self.selected_spaceship]
        name_text = name_font.render(current_spaceship['name'], True, settings.WHITE)
        name_rect = name_text.get_rect(topleft=(info_x, info_y))
        self.screen.blit(name_text, name_rect)

        info_titles = ["Damage", "Speed", "Reload Rate", "Health"]  # Add "Health" to the info titles
        info_values = [
            current_spaceship['damage'],
            current_spaceship['speed'],
            current_spaceship['reload_rate'],
            current_spaceship['health']  # Add the health value to the info values
        ]

        for i, (title, value) in enumerate(zip(info_titles, info_values)):
            draw_info_box(self.screen, title, value, info_x, info_y + 40 + i * 30)

        padding = 10  # Adjust this value to change the spacing/padding

        for i, spaceship in enumerate(self.spaceship_images):
            small_spaceship = pygame.transform.scale(spaceship, (64, 64))
            x = (i % 4) * (64 + 20) + (settings.SCREEN_WIDTH - (64 * 4 + 20 * 3)) // 2
            y = settings.SCREEN_HEIGHT - 100 - padding
            self.screen.blit(small_spaceship, (x, y))

            if i == self.selected_spaceship:
                pygame.draw.line(self.screen, settings.WHITE, (x, y + 64 + padding), (x + 64, y + 64 + padding), 1)

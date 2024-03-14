import pygame
from shared import game_settings as settings
from shared.scene import Scene

class SpaceshipSelection(Scene):

    def __init__(self, screen):
        super().__init__(screen)  # Call the parent class constructor
        self.screen = screen
        self.spaceships = [
            {"image": "assets/spaceships/spaceship1.png", "name": "Sparrow", "damage": 10, "speed": 5, "reload_rate": 1},
            {"image": "assets/spaceships/spaceship2.png", "name": "Phoenix", "damage": 15, "speed": 4, "reload_rate": 0.8},
            {"image": "assets/spaceships/spaceship3.png", "name": "Falcon", "damage": 12, "speed": 6, "reload_rate": 1.2},
            {"image": "assets/spaceships/spaceship4.png", "name": "Eagle", "damage": 8, "speed": 7, "reload_rate": 0.9}
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
        self.next_scene = None  # Reset the next_scene attribute


    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_spaceship = (self.selected_spaceship - 1) % len(self.spaceships)
            elif event.key == pygame.K_RIGHT:
                self.selected_spaceship = (self.selected_spaceship + 1) % len(self.spaceships)
            elif event.key == pygame.K_RETURN:
                self.switch_to_scene("game")  # Use the switch_to_scene method


    def update(self, dt):
        pass

    def draw(self):
        self.screen.fill(settings.BLACK)
        
        title_font = pygame.font.SysFont(None, 36)
        title_text = title_font.render("Select Your Ship", True, settings.WHITE)
        title_rect = title_text.get_rect(centerx=settings.SCREEN_WIDTH // 2, y=20)
        self.screen.blit(title_text, title_rect)
        
        current_image = self.scaled_images[self.selected_spaceship]
        x = settings.SCREEN_WIDTH // 2 - current_image.get_width() // 2
        y = 80
        self.screen.blit(current_image, (x, y))

        info_x = settings.SCREEN_WIDTH // 2 - 150
        info_y = settings.SCREEN_HEIGHT // 2
        
        name_font = pygame.font.SysFont(None, 32)
        current_spaceship = self.spaceships[self.selected_spaceship]
        name_text = name_font.render(current_spaceship['name'], True, settings.WHITE)
        name_rect = name_text.get_rect(topleft=(info_x, info_y))
        self.screen.blit(name_text, name_rect)
        
        info_font = pygame.font.SysFont(None, 24)
        info_titles = ["Damage:", "Speed:", "Reload Rate:"]
        info_values = [str(current_spaceship['damage']), str(current_spaceship['speed']), str(current_spaceship['reload_rate'])]
        
        for i, (title, value) in enumerate(zip(info_titles, info_values)):
            title_text = info_font.render(title, True, settings.GREY)
            value_text = info_font.render(value, True, settings.WHITE)
            title_rect = title_text.get_rect(topleft=(info_x, info_y + 40 + i * 30))
            value_rect = value_text.get_rect(topright=(info_x + 200, info_y + 40 + i * 30))
            self.screen.blit(title_text, title_rect)
            self.screen.blit(value_text, value_rect)

        padding = 10  # Adjust this value to change the spacing/padding

        for i, spaceship in enumerate(self.spaceship_images):
            small_spaceship = pygame.transform.scale(spaceship, (64, 64))
            x = (i % 4) * (64 + 20) + (settings.SCREEN_WIDTH - (64 * 4 + 20 * 3)) // 2
            y = settings.SCREEN_HEIGHT - 100 - padding
            self.screen.blit(small_spaceship, (x, y))

            if i == self.selected_spaceship:
                pygame.draw.line(self.screen, settings.WHITE, (x, y + 64 + padding), (x + 64, y + 64 + padding), 1)
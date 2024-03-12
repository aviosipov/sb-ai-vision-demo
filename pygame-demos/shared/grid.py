import pygame
from shared import game_settings as settings

def draw_text(screen, text, x, y, color=settings.GREY, font_size=34):
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)

def draw_grid(screen):
    column_width = settings.SCREEN_WIDTH / settings.GRID_COLUMNS
    row_height = settings.SCREEN_HEIGHT / settings.GRID_ROWS

    # Draw vertical lines for the grid
    for col in range(settings.GRID_COLUMNS + 1):
        pygame.draw.line(screen, settings.GREY, (col * column_width, 0), (col * column_width, settings.SCREEN_HEIGHT))

    # Draw horizontal lines for the grid
    for row in range(settings.GRID_ROWS + 1):
        pygame.draw.line(screen, settings.GREY, (0, row * row_height), (settings.SCREEN_WIDTH, row * row_height))

    # Draw text in each cell
    for col in range(settings.GRID_COLUMNS):
        for row in range(settings.GRID_ROWS):
            cell_text = f"{row},{col}"
            text_x = col * column_width + column_width / 2
            text_y = row * row_height + row_height / 2
            draw_text(screen, cell_text, text_x, text_y, settings.GREY)
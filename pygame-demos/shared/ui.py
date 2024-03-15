import pygame
from shared import game_settings as settings
from shared.font import load_font

def draw_info_box(screen, title, value, x, y):
    title_font = load_font(18)
    value_font = load_font(24)

    title_text = title_font.render(title, True, settings.GREY)
    value_text = value_font.render(str(value), True, settings.WHITE)

    title_rect = title_text.get_rect(topleft=(x, y))
    value_rect = value_text.get_rect(topleft=(x, y + 25))

    screen.blit(title_text, title_rect)
    screen.blit(value_text, value_rect)

def draw_rectangle(screen, x, y, width, height, color, opacity=255):
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect_surface.fill(color + (opacity,))
    screen.blit(rect_surface, (x, y))

import pygame
from shared import game_settings as settings
from shared.font import load_font

def draw_info_box(screen, title, value, x, y, title_width=135):

    title_font = load_font(12)
    value_font = load_font(14)

    title_text = title_font.render(title, True, settings.LIGHT_GREY)
    value_text = value_font.render(str(value), True, settings.WHITE)

    title_rect = title_text.get_rect(topleft=(x, y))
    value_rect = value_text.get_rect(topleft=(x + title_width, y))

    screen.blit(title_text, title_rect)
    screen.blit(value_text, value_rect)

def draw_rectangle(screen, x, y, width, height, color, opacity=255):
    rect_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    rect_surface.fill(color + (opacity,))
    screen.blit(rect_surface, (x, y))


def draw_breathing_text(screen, text, color, center, breathing_duration, timer):
    font = load_font(18)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=center)
    text_alpha = int(255 * (1 - (timer / breathing_duration)))
    text_surface.set_alpha(text_alpha)
    screen.blit(text_surface, text_rect)
# shared/scene_utils.py
import pygame

def handle_scene_restart(event, reset_func):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
        reset_func()
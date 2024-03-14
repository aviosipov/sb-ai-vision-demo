import pygame
import json
import math
import random

# Initialize Pygame
pygame.init()

# Set the window size
window_size = (800, 600)
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Butterfly Animation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Load the animation data from JSON
animation_data = [
    {"object": "circle", "position": [50, 550], "size": 10, "time": 0, "pen_down": True, "weight": 1},
    {"object": "circle", "position": [100, 500], "size": 12, "time": 10, "pen_down": True, "weight": 1},
    {"object": "circle", "position": [150, 450], "size": 14, "time": 20, "pen_down": True, "weight": 1},
    {"object": "circle", "position": [200, 400], "size": 16, "time": 30, "pen_down": True, "weight": 1},
    {"object": "circle", "position": [250, 350], "size": 18, "time": 40, "pen_down": False, "weight": 2},
    {"object": "circle", "position": [300, 300], "size": 20, "time": 50, "pen_down": False, "weight": 2},
    {"object": "circle", "position": [350, 250], "size": 22, "time": 60, "pen_down": True, "weight": 3},
    {"object": "circle", "position": [400, 200], "size": 24, "time": 70, "pen_down": True, "weight": 3},
    {"object": "circle", "position": [450, 150], "size": 26, "time": 80, "pen_down": True, "weight": 4},
    {"object": "circle", "position": [500, 100], "size": 28, "time": 90, "pen_down": True, "weight": 4},
    {"object": "circle", "position": [550, 50], "size": 30, "time": 100, "pen_down": True, "weight": 5},
    {"object": "circle", "position": [600, 0], "size": 32, "time": 110, "pen_down": True, "weight": 5},
]

def draw_shape(shape, position, size):
    if shape == "circle":
        pygame.draw.circle(screen, BLACK, position, size, 1)
    elif shape == "rectangle":
        pygame.draw.rect(screen, BLACK, (position[0], position[1], size, size), 1)
    elif shape == "square":
        pygame.draw.rect(screen, BLACK, (position[0], position[1], size, size), 1)

def animate_shape(start_pos, end_pos, start_size, end_size, start_time, end_time, current_time, pen_down, weight):
    if current_time >= end_time:
        return end_pos, end_size
    else:
        progress = (current_time - start_time) / (end_time - start_time)
        x = start_pos[0] + progress * (end_pos[0] - start_pos[0])
        y = start_pos[1] + progress * (end_pos[1] - start_pos[1])
        size = start_size + progress * (end_size - start_size)
        
        # Add random perturbations to the position
        x += random.randint(-5, 5)
        y += random.randint(-5, 5)
        
        # Add vertical oscillation
        y += 20 * math.sin(progress * 2 * math.pi)
        
        # Apply gravity based on weight
        y += weight * progress
        
        if pen_down:
            pygame.draw.line(screen, BLACK, start_pos, (x, y), 1)
        
        return [int(x), int(y)], int(size)

# Game loop
running = True
clock = pygame.time.Clock()
frame_count = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)

    current_shape_index = None
    for i in range(len(animation_data)):
        if frame_count >= animation_data[i]["time"]:
            current_shape_index = i
        else:
            break

    if current_shape_index is not None:
        current_shape = animation_data[current_shape_index]
        if current_shape_index < len(animation_data) - 1:
            next_shape = animation_data[current_shape_index + 1]
            position, size = animate_shape(current_shape["position"], next_shape["position"], current_shape["size"], next_shape["size"], current_shape["time"], next_shape["time"], frame_count, current_shape["pen_down"], current_shape["weight"])
        else:
            position, size = current_shape["position"], current_shape["size"]
        draw_shape(current_shape["object"], position, size)

    pygame.display.flip()
    clock.tick(60)
    frame_count += 1

# Quit the game
pygame.quit()
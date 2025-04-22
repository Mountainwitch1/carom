import pygame
import math
import sys
import random

# Initialize pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carrom Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BROWN = (139, 69, 19)
RED = (255, 0, 0)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Board setup
BOARD_MARGIN = 50
BOARD_WIDTH = WIDTH - 2 * BOARD_MARGIN

# Striker settings
striker_radius = 15
striker_pos = [WIDTH // 2, HEIGHT - 100]
striker_color = BLUE
striker_velocity = [0, 0]

# Dragging logic
dragging = False
mouse_start = (0, 0)

# Pockets
pocket_radius = 20
pockets = [
    (BOARD_MARGIN, BOARD_MARGIN),
    (WIDTH - BOARD_MARGIN, BOARD_MARGIN),
    (BOARD_MARGIN, HEIGHT - BOARD_MARGIN),
    (WIDTH - BOARD_MARGIN, HEIGHT - BOARD_MARGIN),
]

# Coin setup
coin_radius = 10
coins = []

center_x, center_y = WIDTH // 2, HEIGHT // 2

# Add red queen in center
coins.append({'pos': [center_x, center_y], 'color': RED})

# Place coins in circular pattern (black and white coins)
def place_ring(radius, num_coins, colors):
    angle_step = 360 / num_coins
    for i in range(num_coins):
        angle = math.radians(i * angle_step)
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        color = colors[i % len(colors)]
        coins.append({'pos': [x, y], 'color': color})

# 12 coins in inner ring (6 white, 6 black)
place_ring(25, 12, [WHITE, BLACK])

# 6 coins in outer ring (3 white, 3 black)
place_ring(50, 6, [WHITE, BLACK])

# Draw board
def draw_board():
    screen.fill(BROWN)
    pygame.draw.rect(screen, WHITE, (BOARD_MARGIN, BOARD_MARGIN, BOARD_WIDTH, BOARD_WIDTH), 5)
    for pocket in pockets:
        pygame.draw.circle(screen, BLACK, pocket, pocket_radius)

# Draw striker
def draw_striker():
    pygame.draw.circle(screen, striker_color, (int(striker_pos[0]), int(striker_pos[1])), striker_radius)

# Draw coins
def draw_coins():
    for coin in coins:
        pygame.draw.circle(screen, coin['color'], (int(coin['pos'][0]), int(coin['pos'][1])), coin_radius)

# Bounce off wall
def check_wall_collision():
    left = BOARD_MARGIN + striker_radius
    right = WIDTH - BOARD_MARGIN - striker_radius
    top = BOARD_MARGIN + striker_radius
    bottom = HEIGHT - BOARD_MARGIN - striker_radius

    if striker_pos[0] < left:
        striker_pos[0] = left
        striker_velocity[0] *= -1
    elif striker_pos[0] > right:
        striker_pos[0] = right
        striker_velocity[0] *= -1

    if striker_pos[1] < top:
        striker_pos[1] = top
        striker_velocity[1] *= -1
    elif striker_pos[1] > bottom:
        striker_pos[1] = bottom
        striker_velocity[1] *= -1

# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    draw_board()
    draw_striker()
    draw_coins()

    # Update striker position
    striker_pos[0] += striker_velocity[0]
    striker_pos[1] += striker_velocity[1]

    # Apply friction
    striker_velocity[0] *= 0.98
    striker_velocity[1] *= 0.98

    # Wall collision
    check_wall_collision()

    # Stop movement if very slow
    if abs(striker_velocity[0]) < 0.1 and abs(striker_velocity[1]) < 0.1:
        striker_velocity = [0, 0]

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            dx = mouse_x - striker_pos[0]
            dy = mouse_y - striker_pos[1]
            distance = math.hypot(dx, dy)

            if distance <= striker_radius:
                dragging = True
                mouse_start = (mouse_x, mouse_y)

        elif event.type == pygame.MOUSEBUTTONUP:
            if dragging:
                mouse_end = pygame.mouse.get_pos()
                dx = mouse_start[0] - mouse_end[0]
                dy = mouse_start[1] - mouse_end[1]
                striker_velocity = [dx * 0.1, dy * 0.1]
                dragging = False

    # Draw aiming line
    if dragging:
        current_mouse = pygame.mouse.get_pos()
        pygame.draw.line(screen, RED, striker_pos, current_mouse, 2)

    pygame.display.flip()

pygame.quit()
sys.exit()

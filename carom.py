import pygame
import math
import sys

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

# Clock
clock = pygame.time.Clock()
FPS = 60

# Board setup
BOARD_MARGIN = 50
BOARD_WIDTH = WIDTH - 2 * BOARD_MARGIN

# Striker settings
striker_radius = 15
striker_pos = [WIDTH // 2, HEIGHT - 100]
striker_color = (50, 50, 255)
striker_velocity = [0, 0]

# Pockets (for now, just circles)
pocket_radius = 20
pockets = [
    (BOARD_MARGIN, BOARD_MARGIN),
    (WIDTH - BOARD_MARGIN, BOARD_MARGIN),
    (BOARD_MARGIN, HEIGHT - BOARD_MARGIN),
    (WIDTH - BOARD_MARGIN, HEIGHT - BOARD_MARGIN),
]


def draw_board():
    screen.fill(BROWN)
    pygame.draw.rect(screen, WHITE, (BOARD_MARGIN, BOARD_MARGIN, BOARD_WIDTH, BOARD_WIDTH), 5)
    for pocket in pockets:
        pygame.draw.circle(screen, BLACK, pocket, pocket_radius)


def draw_striker():
    pygame.draw.circle(screen, striker_color, (int(striker_pos[0]), int(striker_pos[1])), striker_radius)


# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill((0, 0, 0))
    draw_board()
    draw_striker()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
sys.exit()

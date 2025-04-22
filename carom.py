import pygame
import math
import random

# Setup
pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carom Prototype")

FPS = 60
WHITE = (255, 255, 255)
GREEN = (30, 120, 60)
RED = (200, 0, 0)
BLACK = (0, 0, 0)

class Coin:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.radius = radius
        self.color = color
        self.mass = 1

    def draw(self, win):
        pygame.draw.circle(win, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.vx
        self.y += self.vy
        # Friction
        self.vx *= 0.99
        self.vy *= 0.99
        # Stop small movement
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0
        # Bounce walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1

    def collide(self, other):
        dx = other.x - self.x
        dy = other.y - self.y
        dist = math.hypot(dx, dy)
        if dist < self.radius + other.radius:
            # Normalize direction
            nx = dx / dist
            ny = dy / dist

            # Relative velocity
            dvx = self.vx - other.vx
            dvy = self.vy - other.vy

            # Dot product
            dot = dvx * nx + dvy * ny

            # Bounce if moving toward each other
            if dot > 0:
                return

            # Elastic collision
            impulse = 2 * dot / (self.mass + other.mass)
            self.vx -= impulse * other.mass * nx
            self.vy -= impulse * other.mass * ny
            other.vx += impulse * self.mass * nx
            other.vy += impulse * self.mass * ny

# Striker
striker = Coin(WIDTH // 2, HEIGHT - 100, 20, WHITE)

# Coins (white + red)
coins = [
    striker,
    Coin(400, 300, 15, RED),
    Coin(430, 300, 15, BLACK),
    Coin(370, 300, 15, WHITE),
]

aiming = False
shoot_vec = (0, 0)

# Game Loop
run = True
clock = pygame.time.Clock()

while run:
    clock.tick(FPS)
    WIN.fill(GREEN)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if striker.vx == 0 and striker.vy == 0:
                aiming = True
                aim_start = pygame.mouse.get_pos()

        elif event.type == pygame.MOUSEBUTTONUP:
            if aiming:
                aiming = False
                aim_end = pygame.mouse.get_pos()
                dx = aim_start[0] - aim_end[0]
                dy = aim_start[1] - aim_end[1]
                striker.vx = dx / 10
                striker.vy = dy / 10

    # Update + Draw coins
    for coin in coins:
        coin.move()
        coin.draw(WIN)

    # Handle collisions
    for i in range(len(coins)):
        for j in range(i+1, len(coins)):
            coins[i].collide(coins[j])

    # Draw aiming line
    if aiming:
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(WIN, WHITE, (striker.x, striker.y), mouse_pos, 2)

    pygame.display.update()

pygame.quit()

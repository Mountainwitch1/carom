import pygame
import math
import random
import sys

pygame.init()
WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Carrom Game")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
RED = (200, 0, 0)
GRAY = (100, 100, 100)
BG = (240, 200, 140)
BLUE = (30, 144, 255)
GREEN = (0, 200, 0)

# Game settings
FRICTION = 0.985
POCKET_RADIUS = 30
COIN_RADIUS = 12
STRIKER_RADIUS = 18
BORDER_MARGIN = 40

# Classes
class Coin:
    def __init__(self, x, y, color, is_striker=False):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.radius = STRIKER_RADIUS if is_striker else COIN_RADIUS
        self.is_striker = is_striker
        self.pocketed = False

    def move(self):
        if self.pocketed:
            return
        self.x += self.vx
        self.y += self.vy
        self.vx *= FRICTION
        self.vy *= FRICTION
        if abs(self.vx) < 0.05:
            self.vx = 0
        if abs(self.vy) < 0.05:
            self.vy = 0
        self.check_border()

    def draw(self, surface):
        if not self.pocketed:
            pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
            # Spin effect for coins
            if not self.is_striker:
                angle = (pygame.time.get_ticks() // 10) % 360
                spin_length = self.radius - 4
                end_x = int(self.x + spin_length * math.cos(math.radians(angle)))
                end_y = int(self.y + spin_length * math.sin(math.radians(angle)))
                pygame.draw.line(surface, BLACK, (int(self.x), int(self.y)), (end_x, end_y), 2)

    def is_moving(self):
        return abs(self.vx) > 0.1 or abs(self.vy) > 0.1

    def check_border(self):
        if self.x - self.radius < BORDER_MARGIN or self.x + self.radius > WIDTH - BORDER_MARGIN:
            self.vx = -self.vx
        if self.y - self.radius < BORDER_MARGIN or self.y + self.radius > HEIGHT - BORDER_MARGIN:
            self.vy = -self.vy

    def check_pocket(self):
        pockets = [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]
        for px, py in pockets:
            if math.hypot(self.x - px, self.y - py) < POCKET_RADIUS:
                self.pocketed = True
                self.vx = self.vy = 0
                return True
        return False

# Game setup functions
def setup_coins():
    coins = []
    cx, cy = WIDTH // 2, HEIGHT // 2
    for i in range(9):
        angle = math.radians(i * 40)
        coins.append(Coin(cx + 30 * math.cos(angle), cy + 30 * math.sin(angle), WHITE))
    for i in range(9):
        angle = math.radians(i * 40 + 20)
        coins.append(Coin(cx + 50 * math.cos(angle), cy + 50 * math.sin(angle), BLACK))
    coins.append(Coin(cx, cy, RED))  # Red Queen
    return coins

def handle_collisions(coins):
    for i in range(len(coins)):
        for j in range(i+1, len(coins)):
            a, b = coins[i], coins[j]
            if a.pocketed or b.pocketed:
                continue
            dx, dy = b.x - a.x, b.y - a.y
            dist = math.hypot(dx, dy)
            if dist < a.radius + b.radius and dist != 0:
                nx, ny = dx / dist, dy / dist
                overlap = (a.radius + b.radius - dist) / 2
                a.x -= nx * overlap
                a.y -= ny * overlap
                b.x += nx * overlap
                b.y += ny * overlap
                # Elastic collision
                mass_a = a.radius
                mass_b = b.radius
                rel_vx = a.vx - b.vx
                rel_vy = a.vy - b.vy
                dot = rel_vx * nx + rel_vy * ny

                if dot > 0:
                    impulse = 2 * dot / (mass_a + mass_b)
                    a.vx -= impulse * mass_b * nx
                    a.vy -= impulse * mass_b * ny
                    b.vx += impulse * mass_a * nx
                    b.vy += impulse * mass_a * ny

def all_stopped(coins):
    return all(not coin.is_moving() for coin in coins)

def draw_board():
    screen.fill(BG)
    pygame.draw.rect(screen, GRAY, (BORDER_MARGIN, BORDER_MARGIN, WIDTH - 2*BORDER_MARGIN, HEIGHT - 2*BORDER_MARGIN), 8)
    for pos in [(0, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH, HEIGHT)]:
        pygame.draw.circle(screen, BLACK, pos, POCKET_RADIUS)

def show_text(text, x, y, color=BLACK, size=32):
    font = pygame.font.SysFont("Arial", size)
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

def ai_strike(striker, coins, color):
    targets = [c for c in coins if not c.pocketed and c.color == color]
    if targets:
        target = random.choice(targets)
        dx, dy = target.x - striker.x, target.y - striker.y
        angle = math.atan2(dy, dx)
        striker.vx = 10 * math.cos(angle)
        striker.vy = 10 * math.sin(angle)

# Main Menu function with key press handling
def main_menu():
    screen.fill(BG)
    show_text("Carrom Game", WIDTH//2 - 100, HEIGHT//3, RED, 48)
    show_text("1. Human vs Human", WIDTH//2 - 120, HEIGHT//2, BLACK)
    show_text("2. Human vs AI", WIDTH//2 - 120, HEIGHT//2 + 40, BLACK)
    pygame.display.flip()

    choice = None
    while choice not in [1, 2]:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # Option 1
                    choice = 1
                elif event.key == pygame.K_2:  # Option 2
                    choice = 2

    return choice

# Pause Menu
def pause_menu():
    paused = True
    font = pygame.font.SysFont("Arial", 36)
    while paused:
        screen.fill(BG)
        show_text("Game Paused", WIDTH // 2 - 100, HEIGHT // 3, RED, 48)
        show_text("Press 'R' to Restart", WIDTH // 2 - 120, HEIGHT // 2, BLUE, 36)
        show_text("Press 'Q' to Quit", WIDTH // 2 - 120, HEIGHT // 2 + 50, BLUE, 36)
        show_text("Press 'P' to Resume", WIDTH // 2 - 120, HEIGHT // 2 + 100, BLUE, 36)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = False  # Resume game
                elif event.key == pygame.K_r:
                    return "restart"  # Restart the game
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

# Game loop
def game_loop():
    mode = main_menu()
    p1_name = input("Enter Player 1 Name: ")
    p2_name = "AI" if mode == 2 else input("Enter Player 2 Name: ")

    coins = setup_coins()
    striker = Coin(WIDTH // 2, HEIGHT - 60, GRAY, is_striker=True)

    scores = {WHITE: 0, BLACK: 0}
    player_colors = [WHITE, BLACK]
    players = [p1_name, p2_name]
    current = 0
    striker_ready = True
    charging = False
    power = 0
    queen_pocketed = False
    queen_cover_required = None
    queen_temp_storage = None

    running = True
    while running:
        clock.tick(60)
        draw_board()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if striker_ready and current == 0:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    charging = True
                    power = 0
                if event.type == pygame.MOUSEBUTTONUP and charging:
                    charging = False
                    mx, my = pygame.mouse.get_pos()
                    angle = math.atan2(my - striker.y, mx - striker.x)
                    striker.vx = math.cos(angle) * power
                    striker.vy = math.sin(angle) * power
                    striker_ready = False
                    power = 0  # Reset power
                if charging:
                    mx, my = pygame.mouse.get_pos()
                    power = min(math.hypot(mx - striker.x, my - striker.y) / 5, 15)

        for coin in coins:
            coin.move()
            coin.check_pocket()
            coin.draw(screen)

        striker.move()
        striker.draw(screen)

        if all_stopped(coins):
            striker_ready = True
            current = 1 - current  # Switch turn

        handle_collisions(coins)

        pygame.display.flip()

# Start the game
if __name__ == "__main__":
    game_loop()

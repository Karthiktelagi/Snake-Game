import pygame
import sys
import random

# Initialize pygame
pygame.init()
pygame.font.init()

# Game settings
WIDTH, HEIGHT = 1000, 800
GRID_SIZE = 25
SNAKE_SIZE = 25
FPS = 10

# Colors
BLACK = (18, 18, 18)
RED = (255, 70, 70)
GREEN = (0, 255, 100)
WHITE = (240, 240, 240)
GRID_COLOR = (50, 50, 50)

# Fonts
font = pygame.font.Font(None, 45)
big_font = pygame.font.Font(None, 90)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    def get_head_position(self):
        return self.positions[0]

    def update(self):
        cur = self.get_head_position()
        dir_x, dir_y = self.direction
        new = (
            (cur[0] + (dir_x * GRID_SIZE)) % WIDTH,
            (cur[1] + (dir_y * GRID_SIZE)) % HEIGHT
        )

        # Collision check (self bite)
        if len(self.positions) > 2 and new in self.positions[2:]:
            return True  # Game over
        else:
            self.positions.insert(0, new)
            self.positions = self.positions[:self.length]
            return False

    def reset(self):
        self.length = 1
        self.positions = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    def render(self, surface):
        for p in self.positions:
            pygame.draw.rect(surface, self.color,
                             (p[0], p[1], SNAKE_SIZE, SNAKE_SIZE),
                             border_radius=8)


class Fruit:
    def __init__(self):
        self.color = RED
        self.randomize_position()

    def randomize_position(self):
        self.position = (
            random.randint(0, (WIDTH // GRID_SIZE) - 1) * GRID_SIZE,
            random.randint(0, (HEIGHT // GRID_SIZE) - 1) * GRID_SIZE
        )

    def render(self, surface):
        pygame.draw.circle(surface, self.color,
                           (self.position[0] + GRID_SIZE // 2,
                            self.position[1] + GRID_SIZE // 2),
                           GRID_SIZE // 2 - 2)


def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            pygame.draw.rect(surface, GRID_COLOR, (x, y, GRID_SIZE, GRID_SIZE), 1)


def draw_text(surface, text, size, color, pos):
    font_obj = pygame.font.Font(None, size)
    label = font_obj.render(text, True, color)
    rect = label.get_rect(center=pos)
    surface.blit(label, rect)


def game_over_screen(screen, score):
    surface = pygame.Surface(screen.get_size()).convert()
    surface.fill(BLACK)
    draw_text(surface, "💀 GAME OVER 💀", 100, RED, (WIDTH // 2, HEIGHT // 3))
    draw_text(surface, f"Score: {score}", 60, WHITE, (WIDTH // 2, HEIGHT // 2))
    draw_text(surface, "Press R to Restart or Q to Quit", 40, GREEN, (WIDTH // 2, HEIGHT // 1.5))
    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    waiting = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("🐍 Snake Game")

    snake = Snake()
    fruit = Fruit()
    score = 0

    while True:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and snake.direction != DOWN:
                    snake.direction = UP
                elif event.key == pygame.K_DOWN and snake.direction != UP:
                    snake.direction = DOWN
                elif event.key == pygame.K_LEFT and snake.direction != RIGHT:
                    snake.direction = LEFT
                elif event.key == pygame.K_RIGHT and snake.direction != LEFT:
                    snake.direction = RIGHT

        # Update snake
        game_over = snake.update()
        if game_over:
            game_over_screen(screen, score)
            snake.reset()
            fruit.randomize_position()
            score = 0

        # Check fruit collision
        if snake.get_head_position() == fruit.position:
            snake.length += 1
            score += 10
            fruit.randomize_position()

        # Rendering
        screen.fill(BLACK)
        draw_grid(screen)
        snake.render(screen)
        fruit.render(screen)
        draw_text(screen, f"Score: {score}", 40, WHITE, (100, 30))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == "__main__":
    main()

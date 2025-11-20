import pygame
import random
import sys
import time

pygame.init()

WIDTH, HEIGHT = 600, 400
CELL_SIZE = 20
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game Extended")

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 60, 60)
YELLOW = (255, 255, 0)
MAGENTA = (255, 0, 255)
WHITE = (255, 255, 255)

FOOD_TYPES = [
    {"color": RED,     "score": 1, "life": 5},   
    {"color": YELLOW,  "score": 2, "life": 7},   
    {"color": MAGENTA, "score": 3, "life": 9},   
]


def reset_game():
    snake = [(100, 100), (80, 100), (60, 100)]
    direction = 'RIGHT'
    score = 0
    level = 1
    speed = 10
    food, food_type, food_spawn_time = generate_food(snake)
    return snake, direction, score, level, speed, food, food_type, food_spawn_time


def generate_food(snake):
    """Generates food that is not on the snake, with random type."""
    while True:
        x = random.randrange(0, WIDTH, CELL_SIZE)
        y = random.randrange(0, HEIGHT, CELL_SIZE)
        if (x, y) not in snake:
            food_type = random.choice(FOOD_TYPES)
            spawn_time = time.time()
            return (x, y), food_type, spawn_time


def draw_text(text, size, color, x, y, center=True):
    font = pygame.font.SysFont(None, size)
    render = font.render(text, True, color)
    rect = render.get_rect()
    if center:
        rect.center = (x, y)
    else:
        rect.topleft = (x, y)
    window.blit(render, rect)


snake, direction, score, level, speed, food, food_type, food_spawn_time = reset_game()
clock = pygame.time.Clock()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP and direction != 'DOWN':
                    direction = 'UP'
                elif event.key == pygame.K_DOWN and direction != 'UP':
                    direction = 'DOWN'
                elif event.key == pygame.K_LEFT and direction != 'RIGHT':
                    direction = 'LEFT'
                elif event.key == pygame.K_RIGHT and direction != 'LEFT':
                    direction = 'RIGHT'
            else:
                if event.key == pygame.K_r:
                    snake, direction, score, level, speed, food, food_type, food_spawn_time = reset_game()
                    game_over = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()

    if not game_over:

        if time.time() - food_spawn_time > food_type["life"]:
            food, food_type, food_spawn_time = generate_food(snake)

        x, y = snake[0]
        if direction == 'UP':
            y -= CELL_SIZE
        elif direction == 'DOWN':
            y += CELL_SIZE
        elif direction == 'LEFT':
            x -= CELL_SIZE
        elif direction == 'RIGHT':
            x += CELL_SIZE

        new_head = (x, y)

        if x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT or new_head in snake:
            game_over = True
        else:
            snake.insert(0, new_head)

            if new_head == food:
                score += food_type["score"]

                if score % 3 == 0:
                    level += 1
                    speed += 2

                food, food_type, food_spawn_time = generate_food(snake)
            else:
                snake.pop()

    window.fill(BLACK)

    for segment in snake:
        pygame.draw.rect(window, GREEN, (*segment, CELL_SIZE, CELL_SIZE))

    pygame.draw.rect(window, food_type["color"], (*food, CELL_SIZE, CELL_SIZE))

    draw_text(f"Score: {score}  Level: {level}", 30, WHITE, 10, 10, center=False)

    if game_over:
        draw_text("GAME OVER", 80, RED, WIDTH // 2, HEIGHT // 2 - 40)
        draw_text("Press R to Restart or Q to Quit", 30, WHITE, WIDTH // 2, HEIGHT // 2 + 30)

    pygame.display.flip()
    clock.tick(speed)

import pygame
import sys
import random

# Game constants
CELL_SIZE = 40
GRID_WIDTH = 30
GRID_HEIGHT = 20
SCREEN_WIDTH = CELL_SIZE * GRID_WIDTH
SCREEN_HEIGHT = CELL_SIZE * GRID_HEIGHT
SNAKE_COLOR = (0, 255, 0)
FOOD_COLOR = (255, 0, 0)
BG_COLOR = (30, 30, 30)
SCORE_COLOR = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake')
clock = pygame.time.Clock()
font = pygame.font.Font('fonts/pixeltype.ttf', 50)


def draw_rect(cell, color):
    x, y = cell
    rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
    pygame.draw.rect(screen, color, rect)


def random_food(snake):
    while True:
        pos = (random.randint(0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1))
        if pos not in snake:
            return pos


def draw_snake(snake):
    for cell in snake:
        draw_rect(cell, SNAKE_COLOR)


def draw_food(food):
    draw_rect(food, FOOD_COLOR)


def draw_score(score):
    text = font.render(f'Score: {score}', True, SCORE_COLOR)
    screen.blit(text, (10, 10))


def game_over_screen(score):
    screen.fill(BG_COLOR)
    over_text = font.render('Game Over!', True, (255, 80, 80))
    score_text = font.render(f'Final Score: {score}', True, SCORE_COLOR)
    restart_text = font.render('Press SPACE to restart', True, (200, 200, 200))
    screen.blit(over_text, (SCREEN_WIDTH//2 - over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
    screen.blit(score_text, (SCREEN_WIDTH//2 - score_text.get_width()//2, SCREEN_HEIGHT//2 - 20))
    screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2 + 40))
    pygame.display.update()


def main():
    snake = [(GRID_WIDTH//2, GRID_HEIGHT//2)]
    direction = (1, 0)
    food = random_food(snake)
    score = 0
    game_over = False
    move_delay = 120  # ms
    last_move = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if game_over:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return  # Restart
            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and direction != (0, 1):
                        direction = (0, -1)
                    elif event.key == pygame.K_DOWN and direction != (0, -1):
                        direction = (0, 1)
                    elif event.key == pygame.K_LEFT and direction != (1, 0):
                        direction = (-1, 0)
                    elif event.key == pygame.K_RIGHT and direction != (-1, 0):
                        direction = (1, 0)

        if not game_over and pygame.time.get_ticks() - last_move > move_delay:
            last_move = pygame.time.get_ticks()
            new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])
            # Check wall collision
            if (not 0 <= new_head[0] < GRID_WIDTH) or (not 0 <= new_head[1] < GRID_HEIGHT):
                game_over = True
            # Check self collision
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)
                if new_head == food:
                    score += 1
                    food = random_food(snake)
                else:
                    snake.pop()

        screen.fill(BG_COLOR)
        draw_snake(snake)
        draw_food(food)
        draw_score(score)
        pygame.display.update()
        clock.tick(60)

        if game_over:
            game_over_screen(score)
            # Wait for restart
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        return


if __name__ == '__main__':
    while True:
        main()

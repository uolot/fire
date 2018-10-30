import pygame
from random import random
from collections import defaultdict
import sys


# updates per second
FRAME_RATE = 20
TILE_SIZE = 20

SCREEN_SIZE = 800, 600
GRID_W = SCREEN_SIZE[0] // TILE_SIZE
GRID_H = SCREEN_SIZE[1] // TILE_SIZE

BLACK = 0, 0, 0


def chance(p):
    p = p / 100
    r = random()
    return 1 if r < p else 0


def new_grid(w, h):
    col = h * [0]
    return [col[:] for _ in range(w)]


def init_grid(grid):
    for x in range(len(grid)):
        grid[x][-1] = int(chance(50))


def iter_grid(grid):
    w = len(grid)
    h = len(grid[0])

    new = new_grid(w, h)

    for x, col in enumerate(grid):
        for y, cell in enumerate(col):

            color = (128 + int(128 * y/GRID_H), 255 - int(255 * y/GRID_H), 0)

            if y == h-1 and chance(90):
                new[x][y] = color
                continue

            if x > 0:
                left_col = grid[x-1]
            else:
                left_col = defaultdict(lambda: 0)

            if x < GRID_W - 1:
                right_col = grid[x+1]
            else:
                right_col = defaultdict(lambda: 0)

            points = 0

            if y > 0:
                top = int(bool(left_col[y-1])) + int(bool(col[y-1])) + int(bool(right_col[y-1]))
                points = top * 1

            middle = int(bool(left_col[y])) + int(bool(right_col[y]))
            points += middle * 2

            if y < GRID_H - 1:
                bottom = int(bool(left_col[y+1])) + int(bool(col[y+1])) + int(bool(right_col[y+1]))
                points += bottom * 3

            if int(points >= 5) and chance(30 + 50 * (y / h)):
                new[x][y] = color

    return new


def draw_grid(grid, screen):
    for x, col in enumerate(grid):
        for y, cell in enumerate(col):
            if cell:
                pygame.draw.rect(
                    screen, cell, pygame.Rect(
                        x * TILE_SIZE, y * TILE_SIZE,
                        TILE_SIZE, TILE_SIZE
                    )
                )


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

grid = new_grid(GRID_W, GRID_H)
init_grid(grid)

done = False
paused = False

export = len(sys.argv) > 1 and sys.argv[1] == '--gif'
count = 0
dirname = 'export'
MAX_FRAMES = 100


while not done:
    for event in pygame.event.get():
        done = event.type == pygame.QUIT
        if not done and event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_ESCAPE, pygame.K_q]:
                done = True
            elif event.key == pygame.K_p:
                paused ^= True

    if not paused:
        screen.fill(BLACK)
        draw_grid(grid, screen)
        grid = iter_grid(grid)
        pygame.display.update()

        if export:
            if count >= MAX_FRAMES:
                done = True
            pygame.image.save(screen, f'{dirname}/{count:02}.png')
            count += 1

    clock.tick(FRAME_RATE)


pygame.quit()

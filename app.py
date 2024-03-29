from collections import defaultdict
import random
import sys

import pygame


# updates per second
FRAME_RATE = 20
TILE_SIZE = 20

SCREEN_SIZE = 800, 600
GRID_W = SCREEN_SIZE[0] // TILE_SIZE
GRID_H = SCREEN_SIZE[1] // TILE_SIZE

SKIP_FRAMES = 50
MAX_FRAMES = 100 + SKIP_FRAMES

BLACK = 0, 0, 0


# game state
done = False
paused = False

# export options
export = len(sys.argv) > 1 and sys.argv[1] == '--gif'
count = 0
dirname = 'export'

# drawing options
shift = False
SHIFT_FACTOR = 0.15

# scaling options
scale = True
MIN_SCALE_FACTOR = 0.5

# shape options
# shape = 'rect'
# shape = 'circle'
shape = 'ellipse'


def chance(p):
    p = p / 100
    r = random.random()
    return 1 if r < p else 0


def random_shift(x, p):
    """Change x by up to p percent (where 0 <= p < 1)"""
    d = x * p
    s = random.random() * 2 * d - d
    return x + s


def new_grid():
    col = GRID_H * [0]
    return [col[:] for _ in range(GRID_W)]


def init_grid(grid):
    for x in range(len(grid)):
        grid[x][-1] = int(chance(50))


def iter_grid(grid):
    new = new_grid()

    for x, col in enumerate(grid):
        for y, cell in enumerate(col):

            # TODO: fix green
            color = (128 + int(128 * y/GRID_H), 255 - int(255 * y/GRID_H), 0)

            if y == GRID_H-1 and chance(90):
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

            if int(points >= 4) and chance(30 + 50 * (y / GRID_H)):
                new[x][y] = color

    return new


def draw_grid(grid, screen):  # noqa (mccabe)
    for x, col in enumerate(grid):
        for y, cell in enumerate(col):
            if cell:
                cx, cy = x * TILE_SIZE, y * TILE_SIZE
                if shift:
                    cx = cx + int(random_shift(TILE_SIZE, SHIFT_FACTOR))
                    cy = cy + int(random_shift(TILE_SIZE, SHIFT_FACTOR))

                if scale:
                    yp = y / GRID_H

                if shape == 'rect':
                    cw, ch = TILE_SIZE, TILE_SIZE
                    if scale:
                        cw = cw * (yp + MIN_SCALE_FACTOR)
                        ch = ch * (yp + MIN_SCALE_FACTOR)
                    pygame.draw.rect(
                        screen, cell, pygame.Rect(
                            cx, cy, cw, ch
                        )
                    )

                elif shape == 'circle':
                    r = TILE_SIZE
                    if scale:
                        r = int(TILE_SIZE * (yp + random_shift(0.3, 0.6)))
                    pygame.draw.circle(
                        screen, cell,
                        (cx, cy), r
                    )

                elif shape == 'ellipse':
                    cw, ch = TILE_SIZE * 1.5, TILE_SIZE * 3
                    if scale:
                        cw = cw * (yp + MIN_SCALE_FACTOR)
                        ch = ch * (yp + MIN_SCALE_FACTOR)
                    pygame.draw.ellipse(
                        screen, cell, pygame.Rect(
                            cx, cy, cw, ch
                        )
                    )


pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
clock = pygame.time.Clock()

grid = new_grid()
init_grid(grid)


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
        grid = iter_grid(grid)
        draw_grid(grid, screen)
        pygame.display.update()

        if export:
            if count >= MAX_FRAMES:
                done = True
            elif count >= SKIP_FRAMES:
                n = count - SKIP_FRAMES
                pygame.image.save(screen, f'{dirname}/{n:02}.png')
            count += 1

    clock.tick(FRAME_RATE)


pygame.quit()

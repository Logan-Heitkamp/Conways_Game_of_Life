import pygame as pg
import sys

def draw_screen(this_screen, camera_pos: list[int], grid_size: int, tiles: list[list[int]]) -> None:
    this_screen.fill((100, 100, 100))

    for tile in tiles:
        pg.draw.rect(this_screen, (255, 255, 255), pg.Rect((tile[0] * grid_size) + camera_pos[0], (tile[1] * grid_size) + camera_pos[1], grid_size, grid_size))


    for x in range(1200):
        if x % grid_size == 0:
            pg.draw.rect(this_screen, (0, 0, 0), pg.Rect(x + (camera_pos[0] % grid_size), 0, 1, 800))

    for y in range(800):
        if y % grid_size == 0:
            pg.draw.rect(this_screen, (0, 0, 0), pg.Rect(0, y + (camera_pos[1] % grid_size), 1200, 1))

    pg.draw.circle(this_screen, (255, 0, 0), (600, 400),3)

    pg.display.flip()

def get_number_around(tiles: list[list[int]], tile: list[int]) -> int:
    num = 0
    x = tile[0]
    y = tile[1]

    surroundings = [[x+1, y-1], [x+1, y], [x+1, y+1], [x, y], [x, y], [x, y], [x, y], [x, y]]

    if [x+1, y+1] in tiles:
        num += 1
    if [x, y+1] in tiles:
        num += 1
    if [x-1, y+1] in tiles:
        num += 1
    if [x+1, y] in tiles:
        num += 1
    if [x-1, y] in tiles:
        num += 1
    if [x+1, y-1] in tiles:
        num += 1
    if [x, y-1] in tiles:
        num += 1
    if [x-1, y-1] in tiles:
        num += 1

    return num

if __name__ == "__main__":

    # Setup Pygame
    pg.init()
    width, height = 1200, 800
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("My pg Template")
    clock = pg.time.Clock()
    running = True

    # Setup Camera
    camera = [600, 400]
    move_speed = 1
    zoom = 50

    grid = [[0, 0], [1, 0], [-1, 0], [0, -1], [0, 1]]
    frame = 0

    # Main game loop
    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEWHEEL:
                if event.y > 0:
                    zoom += 2
                    camera[0] = ((camera[0] - 600) / (zoom - 2)) * zoom + 600
                    camera[1] = ((camera[1] - 400) / (zoom - 2)) * zoom + 400
                if event.y < 0:
                    zoom -= 2
                    if zoom <= 2:
                        zoom = 4
                    else:
                        camera[0] = ((camera[0] - 600) / (zoom + 2)) * zoom + 600
                        camera[1] = ((camera[1] - 400) / (zoom + 2)) * zoom + 400

        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            move_speed = (zoom**1.05 // 4) * 5
        else:
            move_speed = (zoom**1.05 // 4)
        if keys[pg.K_w]:
            camera[1] += move_speed
        if keys[pg.K_a]:
            camera[0] += move_speed
        if keys[pg.K_s]:
            camera[1] -= move_speed
        if keys[pg.K_d]:
            camera[0] -= move_speed

        # only run calculations every 4 frames
        if frame == 3:
            pass
        frame = (frame + 1) % 4

        draw_screen(screen, camera, zoom, grid)

        clock.tick(60)

    # Quit pg
    pg.quit()
    sys.exit()
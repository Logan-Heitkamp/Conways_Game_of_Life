import pygame as pg
import sys

def draw_screen(camera_pos: list[int], grid_size: int) -> None:
    screen.fill((100, 100, 100))

    for x in range(1200):
        if x % grid_size == 0:
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(x + (camera_pos[0] % grid_size), 0, 1, 800))

    for y in range(800):
        if y % grid_size == 0:
            pg.draw.rect(screen, (0, 0, 0), pg.Rect(0, y + (camera_pos[1] % grid_size), 1200, 1))

    pg.display.flip()

if __name__ == "__main__":

    # Setup Pygame
    pg.init()
    width, height = 1200, 800
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("My pg Template")
    clock = pg.time.Clock()
    running = True

    # Setup Camera
    camera = [0, 0]
    move_speed = 1
    zoom = 50

    # Main game loop
    while running:
        # Handle events
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEWHEEL:
                if event.y > 0:
                    zoom += 2
                if event.y < 0:
                    zoom -= 2
                    if zoom <= 2:
                        zoom = 4

        keys = pg.key.get_pressed()
        if keys[pg.K_LSHIFT]:
            move_speed = (zoom // 4) * 5
        else:
            move_speed = (zoom // 4)
        if keys[pg.K_w]:
            camera[1] += move_speed
        if keys[pg.K_a]:
            camera[0] += move_speed
        if keys[pg.K_s]:
            camera[1] -= move_speed
        if keys[pg.K_d]:
            camera[0] -= move_speed

        draw_screen(camera, zoom)

        clock.tick(60)

    # Quit pg
    pg.quit()
    sys.exit()
import pygame as pg
import sys
import random

def draw_screen(this_screen, camera_pos: list[int], tile_size: int, tiles: list[tuple[int, int]]) -> None:
    this_screen.fill((100, 100, 100))

    for tile in tiles:
        pg.draw.rect(this_screen, (255, 255, 255), pg.Rect((tile[0] * tile_size) + camera_pos[0], (tile[1] * tile_size) + camera_pos[1], tile_size, tile_size))

    for x in range(1200):
        if x % tile_size == 0:
            pg.draw.rect(this_screen, (0, 0, 0), pg.Rect(x + (camera_pos[0] % tile_size), 0, 1, 800))

    for y in range(800):
        if y % tile_size == 0:
            pg.draw.rect(this_screen, (0, 0, 0), pg.Rect(0, y + (camera_pos[1] % tile_size), 1200, 1))

    pg.display.flip()

def get_surroundings(tile: tuple[int, int]) -> list[tuple[int, int]]:
    x: int = tile[0]
    y: int = tile[1]
    return [(x+1, y-1), (x+1, y), (x+1, y+1), (x, y-1), (x, y+1), (x-1, y-1), (x-1, y), (x-1, y+1)]

def get_number_surrounding_alive(tiles: dict[tuple[int, int], bool], tile: tuple[int, int]) -> int:
    num = 0
    surroundings = get_surroundings(tile)
    for surrounding_tile in surroundings:
        if surrounding_tile in tiles:
            if tiles[surrounding_tile]:
                num += 1

    return num

def create_dead_tiles(tiles: dict[tuple[int, int], bool]) -> None:
    for each_tile in list(tiles.keys()):
        surroundings = get_surroundings(each_tile)
        for surrounding_tile in surroundings:
            if surrounding_tile not in tiles:
                tiles[surrounding_tile] = False

def update_tiles(tiles: dict[tuple[int, int], bool]) -> None:
    new_tiles = {}
    for each_tile, alive in list(tiles.items()):
        surrounding_alive = get_number_surrounding_alive(tiles, each_tile)
        if surrounding_alive < 2:
            new_tiles[each_tile] = False
        elif surrounding_alive == 3 and not alive:
            new_tiles[each_tile] = True
        elif surrounding_alive > 3:
            new_tiles[each_tile] = False

    tiles.update(new_tiles)

def purge_dead_tiles(tiles: dict[tuple[int, int], bool]) -> None:
    for each_tile, alive in list(tiles.items()):
        if not alive:
            tiles.pop(each_tile)

def get_clicked_tile(pos: tuple[int, int], tile_size: int, camera_pos: list[int]) -> tuple[int, int]:
    x = (pos[0] - camera_pos[0]) / tile_size
    y = (pos[1] - camera_pos[1]) / tile_size

    if x < 0:
        x -= 1
    if y < 0:
        y -= 1

    y = int(y)
    x = int(x)

    return x, y

def change_tile(tiles: dict[tuple[int, int], bool], tile: tuple[int, int]):
    if tile in tiles:
        tiles[tile] = not tiles[tile]
    else:
        tiles[tile] = True
    purge_dead_tiles(tiles)

def randomize(tiles: dict[tuple[int, int], bool]) -> None:
    new_tiles = {}

    for i in range(150):
        for j in range(150):
            new_tiles[(i-75, j-75)] = bool(random.getrandbits(1))

    tiles.update(new_tiles)

if __name__ == "__main__":

    # Setup Pygame
    pg.init()
    width, height = 1200, 800
    screen = pg.display.set_mode((width, height))
    pg.display.set_caption("Conway's Game of Life")
    clock = pg.time.Clock()
    running = True

    # Setup Camera
    camera: list[int] = [600, 400]
    move_speed = 1
    zoom = 50

    grid = {(0, 0): True, (1, -1): True, (2, -1): True, (2, 0): True, (2, 1): True}
    frame = 0
    play = False

    # Main game loop
    while running:
        # Handle events
        for event in pg.event.get():

            # Close Program
            if event.type == pg.QUIT:
                running = False

            # Get key presses
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if play:
                        play = False
                    else:
                        play = True
                if event.key == pg.K_r:
                    randomize(grid)
                    purge_dead_tiles(grid)

            # Handle zoom
            if event.type == pg.MOUSEWHEEL:
                if event.y > 0:
                    zoom += 5
                    camera[0] = ((camera[0] - 600) / (zoom - 5)) * zoom + 600
                    camera[1] = ((camera[1] - 400) / (zoom - 5)) * zoom + 400
                if event.y < 0:
                    zoom -= 5
                    if zoom < 5:
                        zoom = 5
                    else:
                        camera[0] = ((camera[0] - 600) / (zoom + 5)) * zoom + 600
                        camera[1] = ((camera[1] - 400) / (zoom + 5)) * zoom + 400

            # Place tiles
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if not play:
                        mouse_pos = event.pos
                        grid_pos = get_clicked_tile(mouse_pos, zoom, camera)
                        change_tile(grid, grid_pos)

        # Movement Events
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

        # only run game every 4 frames
        if frame == 3 and play:
            create_dead_tiles(grid)
            update_tiles(grid)
            purge_dead_tiles(grid)
        frame = (frame + 1) % 4
        # frame = 3

        draw_screen(screen, camera, zoom, list(grid.keys()))

        clock.tick(60)

    # Quit pg
    pg.quit()
    sys.exit()
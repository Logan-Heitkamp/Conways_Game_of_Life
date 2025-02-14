import main as m
from unittest.mock import patch, MagicMock, call


@patch('pygame.display.flip')
@patch('main.draw_grid')
@patch('main.draw_tiles')
def test_draw_screen(mock_draw_tiles, mock_draw_grid, mock_flip):
    test_screen = MagicMock()
    test_camera = [0, 0]
    test_tile_size = 50
    test_tiles = test_tiles = {(0, 0): True, (1, -1): True, (1, 0): True, (1, 1): True, (0, -1): True, (0, 1): True, (-1, -1): True, (-1, 0): True, (-1, 1): True}

    m.draw_screen(test_screen, test_camera, test_tile_size, list(test_tiles.keys()))
    mock_draw_tiles.assert_called_once_with(test_screen, test_camera, test_tile_size, list(test_tiles.keys()))
    mock_draw_grid.assert_called_once_with(test_screen, test_camera, test_tile_size)

@patch('pygame.Rect')
@patch('pygame.draw.rect')
def test_draw_tiles(mock_draw, mock_rect):
    test_screen = MagicMock()
    test_camera = [1, 1]
    test_tile_size = 50
    test_tiles = {(0, 0): True, (1, -1): True, (1, 0): True, (1, 1): True, (0, -1): True, (0, 1): True, (-1, -1): True, (-1, 0): True, (-1, 1): True}

    m.draw_tiles(test_screen, test_camera, test_tile_size, list(test_tiles.keys()))

    calls = [call(1, 1, test_tile_size, test_tile_size),
             call(51, -49, test_tile_size, test_tile_size),
             call(51, 1, test_tile_size, test_tile_size),
             call(51, 51, test_tile_size, test_tile_size),
             call(1, -49, test_tile_size, test_tile_size),
             call(1, 51, test_tile_size, test_tile_size),
             call(-49, -49, test_tile_size, test_tile_size),
             call(-49, 1, test_tile_size, test_tile_size),
             call(-49, 51, test_tile_size, test_tile_size),]

    mock_rect.assert_has_calls(calls)
    assert mock_rect.call_count == 9

@patch('pygame.Rect')
@patch('pygame.draw.rect')
def test_draw_grid(mock_draw, mock_rect):
    test_screen = MagicMock()
    test_camera = [0, 0]
    test_tile_size = 50

    m.draw_grid(test_screen, test_camera, test_tile_size)
    assert mock_rect.call_count == 40


def test_get_surroundings():
    test_tile = (0, 0)
    ret = m.get_surroundings(test_tile)

    correct_result = [(1, 1), (0, 1), (-1, 1), (1, 0), (-1, 0), (1, -1), (0, -1), (-1, -1)]

    assert (len(ret) == 8)
    for item in correct_result:
        assert item in ret

def test_get_number_surrounding_alive_none():
    test_tiles = {(0, 0): True, (1, -1): False, (1, 0): False, (1, 1): False, (0, -1): False, (0, 1): False, (-1, -1): False, (-1, 0): False, (-1, 1): False}
    test_tile = (0, 0)
    assert m.get_number_surrounding_alive(test_tiles, test_tile) == 0

def test_get_number_surrounding_alive_all():
    test_tiles = {(0, 0): True, (1, -1): True, (1, 0): True, (1, 1): True, (0, -1): True, (0, 1): True, (-1, -1): True, (-1, 0): True, (-1, 1): True}
    test_tile = (0, 0)
    assert m.get_number_surrounding_alive(test_tiles, test_tile) == 8

def test_create_dead_tiles():
    test_tiles = {(0, 0): True}
    m.create_dead_tiles(test_tiles)
    assert test_tiles == {(0, 0): True, (1, -1): False, (1, 0): False, (1, 1): False, (0, -1): False, (0, 1): False, (-1, -1): False, (-1, 0): False, (-1, 1): False}

def test_update_tiles_no_alive():
    test_tiles = {(0, 0): False}
    m.update_tiles(test_tiles)
    assert test_tiles == {(0, 0): False}

def test_update_tiles_kill_alive_none_surrounding():
    test_tiles = {(0, 0): True, (0, 1): False}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_update_tiles_kill_alive_one_surrounding():
    test_tiles = {(0, 0): True, (0, 1): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_update_tiles_birth():
    test_tiles = {(0, 0): False, (0, 1): True, (1, 0): True, (0, -1): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == True

def test_update_tiles_overpopulation_four():
    test_tiles = {(0, 0): True, (0, 1): True, (1, 0): True, (0, -1): True, (-1, 0): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_update_tiles_overpopulation_five():
    test_tiles = {(0, 0): True, (0, 1): True, (1, 0): True, (0, -1): True, (-1, 0): True, (1, 1): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_update_tiles_overpopulation_six():
    test_tiles = {(0, 0): True, (0, 1): True, (1, 0): True, (0, -1): True, (-1, 0): True, (1, 1): True, (1, -1): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_update_tiles_overpopulation_seven():
    test_tiles = {(0, 0): True, (0, 1): True, (1, 0): True, (0, -1): True, (-1, 0): True, (1, 1): True, (1, -1): True, (-1, 1): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_update_tiles_overpopulation_eight():
    test_tiles = {(0, 0): True, (0, 1): True, (1, 0): True, (0, -1): True, (-1, 0): True, (1, 1): True, (1, -1): True, (-1, 1): True, (-1, -1): True}
    m.update_tiles(test_tiles)
    assert test_tiles[(0, 0)] == False

def test_purge_dead_tiles():
    test_tiles = {(0, 0): True, (1, 0): False, (0, 1): True, (-1, 0): False}
    m.purge_dead_tiles(test_tiles)
    assert test_tiles == {(0, 0): True, (0, 1): True}

def test_get_clicked_tile_on_grid():
    test_pos = (0, 0)
    test_tile_size = 50
    test_camera_pos = [0, 0]

    assert m.get_clicked_tile(test_pos, test_tile_size, test_camera_pos) == (0, 0)

def test_get_clicked_tile_off_grid():
    test_pos = (123, 123)
    test_tile_size = 50
    test_camera_pos = [0, 0]

    assert m.get_clicked_tile(test_pos, test_tile_size, test_camera_pos) == (2, 2)

def test_change_tile_not_in_grid():
    test_tiles = {}
    m.change_tile(test_tiles, (0, 0))
    assert test_tiles == {(0, 0): True}

def test_change_tile_to_alive():
    test_tiles = {(0, 0): False}
    m.change_tile(test_tiles, (0, 0))
    assert test_tiles == {(0, 0): True}

def test_change_tile_to_dead():
    test_tiles = {(0, 0): True}
    m.change_tile(test_tiles, (0, 0))
    assert test_tiles == {(0, 0): False}

@patch('random.getrandbits')
def test_randomize_tiles_alive(mock_random):
    mock_random.return_value = 1
    test_tiles = {}
    m.randomize(test_tiles)
    for value in list(test_tiles.values()):
        assert value == True

    assert len(test_tiles) == 22500

@patch('random.getrandbits')
def test_randomize_tiles_dead(mock_random):
    mock_random.return_value = 0
    test_tiles = {}
    m.randomize(test_tiles)
    for value in list(test_tiles.values()):
        assert value == False

    assert len(test_tiles) == 22500


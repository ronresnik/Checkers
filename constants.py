import os

white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
PIECES_IN_ROW = 8
TILES_IN_ROW = 8
PIECES_IN_COLLUMN = 3
TILE_WIDTH = 100
RADIUS = 25
WHITE_BASE = [(i, 0) for i in range(8)]
BLACK_BASE = [(i, 7) for i in range(8)]
RANGE = [(x, y) for x in range(8) for y in range(8)]
rows, cols = (8, 8)
BASE_DIR = os.path.dirname(__file__)

"""[summary]

Raises:
    execption: [description]
    ValueError: [description]

Returns:
    [type]: [description]
"""
import os
import time
from datetime import datetime as dt
import pygame
from piece import Troop, Queen
from constants import WHITE, GREY, BLACK, RED, TILES_IN_ROW, cols, rows, BASE_DIR, TILE_WIDTH


class Board(object):
    """[summary]

    Raises:
        execption: [description]
        ValueError: [description]

    Returns:`
        [type]: [description]
    """

    def __init__(self, _current_troops_array=None, piece=0):
        # set display
        self.gamedisplay = pygame.display.set_mode((800, 800))
        # caption
        self.gamedisplay.fill(WHITE)
        pygame.display.set_caption("Checkers")

        self.piece = piece
        if _current_troops_array == None:
            self._current_troops_array = self._init_troops_array()
        else:
            self._current_troops_array = _current_troops_array
        # self.draw_pieces()

    def get_all_pieces(self, color):
        pieces = []
        for x in range(TILES_IN_ROW):
            for y in range(TILES_IN_ROW):
                if isinstance(self._current_troops_array[x][y], Troop) and self._current_troops_array[x][y].color == color:
                    pieces.append(self._current_troops_array[x][y])
        # return all pices of the color
        return pieces

    def _init_troops_array(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        initial_troops_array = [[0 for i in range(cols)] for j in range(rows)]
        for x in range(TILES_IN_ROW):
            # upper troops
            for y in range(TILES_IN_ROW):
                if (x % 2 == y % 2) and (y < 3 or y > 4):
                    if y < 3:
                        piece_color = "Red"
                        color = RED
                    elif y > 4:
                        piece_color = "Black"
                        color = BLACK
                    piece = Troop(pygame.image.load(os.path.join(BASE_DIR, f"static\\images\\{piece_color}Regular.png")),
                                  True,
                                  x,
                                  y,
                                  (x * TILE_WIDTH) + 25,
                                  (y * TILE_WIDTH) + 25,
                                  color)
                    initial_troops_array[x][y] = piece
        return initial_troops_array

    def to_list(self, src_x="no need", src_y="no need"):
        ggwp = self.troops_array
        if not src_x == src_y == "no need":
            ggwp[src_x][src_y].state = True
        return [ggwp, self.piece]

    def __repr__(self):
        string = ""
        for x in range(TILES_IN_ROW):
            for y in range(TILES_IN_ROW):
                string += f"{self._current_troops_array[y][x].__repr__()}|"
            string += "\n----------------\n"
        return string

    def __setattr__(self, name, value):
        if name == "troops_array":
            self.__dict__["_current_troops_array"] = value
        else:
            self.__dict__[name] = value

    def __getattr__(self, name):
        if name == "troops_array":
            # deepcopying the _current_troops_array
            array = [[0 for i in range(cols)] for j in range(rows)]
            for x in range(TILES_IN_ROW):
                for y in range(TILES_IN_ROW):
                    if isinstance(self._current_troops_array[x][y], Queen):
                        array[x][y] = Queen(*[self._current_troops_array[x][y].__dict__[
                            key] for key in self._current_troops_array[x][y].__dict__.keys() if key != "image"])
                    elif isinstance(self._current_troops_array[x][y], Troop):
                        array[x][y] = Troop(*[self._current_troops_array[x][y].__dict__[
                            key] for key in self._current_troops_array[x][y].__dict__.keys()])
            return array

    def __getitem__(self, indexes):
        return self._current_troops_array[indexes[0]][indexes[1]]

    def __setitem__(self, indexes, data):
        self._current_troops_array[indexes[0]][indexes[1]] = data
        # self.draw_pieces()

    def draw_valid_moves(self, piece, game):
        #t0 = time.perf_counter()
        moves = piece.get_valid_moves(game)
        self.draw_pieces()
        for move in moves:
            row, col = move
            pygame.draw.circle(self.gamedisplay, GREY, (row * TILE_WIDTH +
                                                        TILE_WIDTH//2, col * TILE_WIDTH + TILE_WIDTH//2), 10)
            pygame.display.update()

    def draw_pieces(self):
        """[summary]
        """
        self.gamedisplay.fill(WHITE)
        self.draw_board()
        for column in self._current_troops_array:
            for piece in column:
                if isinstance(piece, Troop) and piece.state:
                    self.gamedisplay.blit(
                        piece.image, (piece.x_picture, piece.y_picture))

        pygame.display.update()

    def draw_board(self):
        """[summary]
        """
        for x in range(TILES_IN_ROW):
            for y in range(TILES_IN_ROW):
                if (x % 2 == 0 and y % 2 != 0) \
                        or (x % 2 != 0 and y % 2 == 0):
                    pygame.draw.rect(
                        self.gamedisplay, BLACK, [(x*TILE_WIDTH), (y*TILE_WIDTH), TILE_WIDTH, TILE_WIDTH])

    def is_loc_free(self, x_dest, y_dest, prevoius=None):
        """[summary]

        Returns:
            [type]: [description]
        """
        # making sure that we dont go back to our prevoius location when multiple eating
        if prevoius is not None:
            if prevoius == (x_dest, y_dest):
                return False
        # if the desired destanation is Troop and the same color of the desired piece to move - flase
        try:
            if isinstance(self._current_troops_array[x_dest][y_dest], Troop):
                # print(x_dest, y_dest, "is taken")
                return False
            return True
        except:
            return False

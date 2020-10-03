"""[summary]

Raises:
    execption: [description]
    ValueError: [description]

Returns:
    [type]: [description]
"""
import os
from datetime import datetime as dt
import pygame
from piece import Troop, Queen
from constants import WHITE, GREY, BLACK, TILES_IN_ROW, cols, rows, PIECES_IN_ROW, PIECES_IN_COLLUMN, BASE_DIR, TILE_WIDTH


class Board(object):
    """[summary]

    Raises:
        execption: [description]
        ValueError: [description]

    Returns:`
        [type]: [description]
    """

    def __init__(self, has_SARUF_suspicous=False, SARUF_suspicous_x=0, SARUF_suspicous_y=0, _current_troops_array=None, piece=0):
        # set display
        self.gamedisplay = pygame.display.set_mode((800, 800))
        # caption
        self.gamedisplay.fill(WHITE)
        pygame.display.set_caption("Checkers")

        self.has_SARUF_suspicous = has_SARUF_suspicous
        self.SARUF_suspicous_x = SARUF_suspicous_x
        self.SARUF_suspicous_y = SARUF_suspicous_y
        self.piece = piece
        if _current_troops_array == None:
            self._current_troops_array = self._init_troops_array()
        else:
            self._current_troops_array = _current_troops_array
        self.draw_pieces()

    def _init_troops_array(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        initial_troops_array = [[0 for i in range(cols)] for j in range(rows)]
        for x in range(PIECES_IN_ROW):
            # upper troops
            for y in range(PIECES_IN_COLLUMN):
                piece = Troop(pygame.image.load(os.path.join(BASE_DIR, "static\\images\\RedRegular.png")),
                              True, x, y, (x *
                                           TILE_WIDTH) + 25,
                              (y * TILE_WIDTH) + 25, "Red")
                initial_troops_array[x][y] = piece
            # lower troops
            for y in range(PIECES_IN_COLLUMN):
                piece = Troop(pygame.image.load(os.path.join(BASE_DIR, "static\\images\\BlackRegular.png")),
                              True, x, y +
                              5, (x * TILE_WIDTH) + 25,
                              ((y+5) * TILE_WIDTH) + 25, "Black")
                initial_troops_array[x][y+5] = piece
                #gamedisplay.blit(piece, ((x * TILE_WIDTH) + 25, ((y + 5) * TILE_WIDTH) + 25))
        return initial_troops_array

    def to_list(self, src_x, src_y):
        ggwp = self.troops_array
        ggwp[src_x][src_y].state = True
        return [self.SARUF_suspicous_x, self.SARUF_suspicous_y, self.has_SARUF_suspicous, ggwp, self.piece]

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
            array = [[0 for i in range(cols)] for j in range(rows)]
            for x in range(TILES_IN_ROW):
                for y in range(TILES_IN_ROW):
                    if isinstance(self._current_troops_array[x][y], Queen):
                        array[x][y] = Queen(*[self._current_troops_array[x][y].__dict__[
                            key] for key in self._current_troops_array[x][y].__dict__.keys() if key != "image"])
                    elif isinstance(self._current_troops_array[x][y], Troop):
                        array[x][y] = Troop(*[self._current_troops_array[x][y].__dict__[
                            key] for key in self._current_troops_array[x][y].__dict__.keys()])
            print("recived new array")
            return array

    def __getitem__(self, indexes):
        return self._current_troops_array[indexes[0]][indexes[1]]

    def __setitem__(self, indexes, data):
        self._current_troops_array[indexes[0]][indexes[1]] = data
        self.draw_pieces()

    def draw_valid_moves(self, piece, game):
        moves = piece.can_advance(
            piece.x, piece.y, game, just_eat=True, get_locs=True)

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

    def is_loc_free(self, x_dest, y_dest):
        """[summary]

        Returns:
            [type]: [description]
        """
        # if the desired destanation is Troop and the same color of the desired piece to move - flase
        if isinstance(self._current_troops_array[x_dest][y_dest], Troop):
            print(x_dest, y_dest, "is taken")
            return False
        return True

    # TODO modify names
    def set_SARUF_suspicous(self, x, y):
        """[summary]

        Args:
            x ([type]): [description]
            y ([type]): [description]
        """
        self.SARUF_suspicous_x = x
        self.SARUF_suspicous_y = y
        self.has_SARUF_suspicous = True

    # FIX
    def suspicous_could_eat(self, x, y):
        """checks if a Troop is elgible for SARUF state
            could eat again and didn't

        Args:
            x ([int]): [description]
            y ([int]): [description]

        Returns:
            [bool]: [description]
        """
        # if original_location is not
        if(self.SARUF_suspicous_x, self.SARUF_suspicous_y) != (x, y):
            self.has_SARUF_suspicous = False
            return True
        return False

    def get_in_between_cordinates(self, src_x, src_y, dst_x, dst_y):
        """if case of an eat move this function return what is the position of the to be eaten piece

        Args:
            src_x ([int]): [the eating troop]
            src_y ([int]): [the eating troop]
            dst_x ([int]): [the eated troop]
            dst_y ([int]): [the eated troop]

        Returns:
            [int tuple]: [if it's not an eat move - then return (0.5,0.5) in order to raise execption, else the location]
        """
        # TODO carefully check for errors
        if (((dst_x-src_x), (dst_y-src_y))
                in [(i, j) for i in range(-1, 2, 2) for j in range(-1, 2, 2)]):
            raise ValueError
        if isinstance(self._current_troops_array[src_x][src_y], Queen):
            ggwp = self.is_only_one_enemy_in_between(
                src_x, src_y, dst_x, dst_y, 1)
            print("ggwpppppp", ggwp)
            return ggwp[0]
        #print("eaten", (int(src_x+((dst_x-src_x)/2)),int(src_y+((dst_y-src_y)/2))))
        return (int(src_x+((dst_x-src_x)/2)),
                int(src_y+((dst_y-src_y)/2)))

    def is_only_one_enemy_in_between(self, src_x, src_y, dst_x, dst_y, code=0):
        """
        checks for amount of pieces in between src and dst

        Returns:
            bool: return true if no troops at all in between or 1 enemy troop
        """
        dat = dt.now()
        # 0:00:00.003471
        # checks that the path is according to damka rules
        # if abs(dst_x-src_x) == abs(dst_y-src_y):
        # the amount of tiles between src and dest \ HEETEK = displacement
        abs_displacement = abs(dst_x-src_x)
        directions = [(x, y) for x in range(-7, 8, 1)
                      for y in range(-7, 8, 1) if abs(x) == abs(y)]

        # constains the troops between the two locations
        in_between_troop_locs = \
            list({(x, y)
                  # Explantaion: for i in range(x_src+(1/-1),dst,(-1/1 - direction of moving))
                  for x in range(src_x+int((dst_x-src_x)/abs_displacement),
                                 dst_x, int((dst_x-src_x)/abs_displacement))
                  for y in range(src_y+int((dst_y-src_y)/abs_displacement),
                                 dst_y, int((dst_y-src_y)/abs_displacement))
                  for dirc in directions
                  # checks if the location generated is abs with the location
                  if (x+dirc[0], y+dirc[1]) in [(src_x, src_y), (dst_x, dst_y)]
                  # checks location is a troop
                  and isinstance(self._current_troops_array[x][y], Troop)})

        print("after: ", in_between_troop_locs)
        print(len(in_between_troop_locs))
        print(dt.now() - dat)
        print(self)
        print(src_x, src_y)

        # code = 1 means were checking if we can eat and we need the cordinits of the to be eaten
        if code == 1:
            if len(in_between_troop_locs) == 0:
                return []
            elif len(in_between_troop_locs) == 1:
                if self._current_troops_array[in_between_troop_locs[0][0]][in_between_troop_locs[0][1]].color == self._current_troops_array[src_x][src_y].color:
                    return []
                # only if theres is precisely 1 ENEMY troop between src and dst then were good
                return in_between_troop_locs
            return []
        # were not checking for eating - but to see if there are 1 or less enemies between src and dst
        else:
            if len(in_between_troop_locs) == 0:
                # so no enemies is GOOD
                return True
            elif len(in_between_troop_locs) == 1:
                if self._current_troops_array[in_between_troop_locs[0][0]][in_between_troop_locs[0][1]].color == self._current_troops_array[src_x][src_y].color:
                    return False
                # and one enemy is good - the rest bad
                return True
            return False

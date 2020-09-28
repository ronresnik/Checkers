"""[summary]

Raises:
    execption: [description]
    ValueError: [description]

Returns:
    [type]: [description]
"""
import os
import copy
from datetime import datetime as dt
import pygame
from Piece import Troop, Queen

counter = 0
# set color with rgb
WHITE, BLACK, REd = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Beginning of logic
BASE_dIR = os.path.dirname(__file__)
GAME_EXIT = False
PIECES_IN_ROW = 8
TILES_IN_ROW = 8
PIECES_IN_COLLUMN = 3
TILE_WIDTH = 100
RADIUS = 25
rows, cols = (8, 8)


class Board(object):
    """[summary]

    Raises:
        execption: [description]
        ValueError: [description]

    Returns:
        [type]: [description]
    """

    def __init__(self, has_SARUF_suspicous=False, SARUF_suspicous_x=0, SARUF_suspicous_y=0, __turn_counter=0, counter=0, _current_troops_array=None):
        # set display
        self.gamedisplay = pygame.display.set_mode((800, 800))
        # caption
        self.gamedisplay.fill(WHITE)
        pygame.display.set_caption("Checkers")

        self.has_SARUF_suspicous = has_SARUF_suspicous
        self.SARUF_suspicous_x = SARUF_suspicous_x
        self.SARUF_suspicous_y = SARUF_suspicous_y
        self.__turn_counter = __turn_counter
        self.counter = counter
        if _current_troops_array == None:
            self._current_troops_array = self.create_initial_troops_pos()
        else:
            self._current_troops_array = _current_troops_array
        self.draw_pieces()

    def to_list(self, src_x_index, src_y_index):
        ggwp = self.troops_array
        ggwp[src_x_index][src_y_index].state = True
        return [self.SARUF_suspicous_x, self.SARUF_suspicous_y, self.has_SARUF_suspicous, self.__turn_counter, self.counter, ggwp]

    def __repr__(self):
        string = ""
        for x_index in range(TILES_IN_ROW):
            for y_index in range(TILES_IN_ROW):
                string += f"{self._current_troops_array[y_index][x_index].__repr__()}|"
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
            for x_index in range(TILES_IN_ROW):
                for y_index in range(TILES_IN_ROW):
                    if isinstance(self._current_troops_array[x_index][y_index], Queen):
                        array[x_index][y_index] = Queen(*[self._current_troops_array[x_index][y_index].__dict__[
                                                        key] for key in self._current_troops_array[x_index][y_index].__dict__.keys() if key != "image"])
                    elif isinstance(self._current_troops_array[x_index][y_index], Troop):
                        array[x_index][y_index] = Troop(*[self._current_troops_array[x_index][y_index].__dict__[
                                                        key] for key in self._current_troops_array[x_index][y_index].__dict__.keys()])
            print("recived new array")
            return array

    def __getitem__(self, indexes):
        return self._current_troops_array[indexes[0]][indexes[1]]

    def __setitem__(self, indexes, data):
        self._current_troops_array[indexes[0]][indexes[1]] = data
        self.draw_pieces()

    def create_initial_troops_pos(self):
        """[summary]

        Returns:
            [type]: [description]
        """
        initial_troops_array = [[0 for i in range(cols)] for j in range(rows)]
        for x_index in range(PIECES_IN_ROW):
            # upper troops
            for y_index in range(PIECES_IN_COLLUMN):
                piece = Troop(pygame.image.load(os.path.join(BASE_dIR, "static\\images\\RedRegular.png")),
                              True, x_index, y_index, (x_index *
                                                       TILE_WIDTH) + 25,
                              (y_index * TILE_WIDTH) + 25, "Red")
                initial_troops_array[x_index][y_index] = piece
            # lower troops
            for y_index in range(PIECES_IN_COLLUMN):
                piece = Troop(pygame.image.load(os.path.join(BASE_dIR, "static\\images\\BlackRegular.png")),
                              True, x_index, y_index +
                              5, (x_index * TILE_WIDTH) + 25,
                              ((y_index+5) * TILE_WIDTH) + 25, "Black")
                initial_troops_array[x_index][y_index+5] = piece
                #gamedisplay.blit(piece, ((x_index * TILE_WIDTH) + 25, ((y_index + 5) * TILE_WIDTH) + 25))
        return initial_troops_array

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

    def update_turn(self, code=1):
        """[summary]
        """
        self.__turn_counter += code
        print(self.__turn_counter)

    def draw_board(self):
        """[summary]
        """
        for x_index in range(TILES_IN_ROW):
            for y_index in range(TILES_IN_ROW):
                if (x_index % 2 == 0 and y_index % 2 != 0) \
                        or (x_index % 2 != 0 and y_index % 2 == 0):
                    pygame.draw.rect(
                        self.gamedisplay, BLACK, [(x_index*TILE_WIDTH), (y_index*TILE_WIDTH), TILE_WIDTH, TILE_WIDTH])

    def it_is_this_color_turn(self, piece):
        """[summary]

        Returns:
            [type]: [description]
        """
        if (self.__turn_counter % 2 == 0 and piece.color == "Red") \
                or (self.__turn_counter % 2 != 0 and piece.color == "Black"):
            print(
                f"Its Player Color {piece.color} Turn. Turn Counter: {self.__turn_counter}")
            return True
        return False

    # TODO modify names
    def set_SARUF_suspicous(self, x_index, y_index):
        """[summary]

        Args:
            x_index ([type]): [description]
            y_index ([type]): [description]
        """
        self.SARUF_suspicous_x = x_index
        self.SARUF_suspicous_y = y_index
        self.has_SARUF_suspicous = True

    # FIX
    def suspicous_could_eat(self, x_index, y_index):
        """checks if a Troop is elgible for SARUF state
            could eat again and didn't

        Args:
            x_index ([int]): [description]
            y_index ([int]): [description]

        Returns:
            [bool]: [description]
        """
        # if original_location is not
        if(self.SARUF_suspicous_x, self.SARUF_suspicous_y) != (x_index, y_index):
            self.has_SARUF_suspicous = False
            return True
        return False

    def get_in_between_cordinates(self, src_x_index, src_y_index, dst_x_index, dst_y_index):
        """if case of an eat move this function return what is the position of the to be eaten piece

        Args:
            src_x_index ([int]): [the eating troop]
            src_y_index ([int]): [the eating troop]
            dst_x_index ([int]): [the eated troop]
            dst_y_index ([int]): [the eated troop]

        Returns:
            [int tuple]: [if it's not an eat move - then return (0.5,0.5) in order to raise execption, else the location]
        """
        # TODO carefully check for errors
        if (((dst_x_index-src_x_index), (dst_y_index-src_y_index))
                in [(i, j) for i in range(-1, 2, 2) for j in range(-1, 2, 2)]):
            raise ValueError
        if isinstance(self._current_troops_array[src_x_index][src_y_index], Queen):
            ggwp = self.is_only_one_enemy_in_between(
                src_x_index, src_y_index, dst_x_index, dst_y_index, 1)
            print("ggwpppppp", ggwp)
            return ggwp[0]
        #print("eaten", (int(src_x_index+((dst_x_index-src_x_index)/2)),int(src_y_index+((dst_y_index-src_y_index)/2))))
        return (int(src_x_index+((dst_x_index-src_x_index)/2)),
                int(src_y_index+((dst_y_index-src_y_index)/2)))

    def is_only_one_enemy_in_between(self, src_x_index, src_y_index, dst_x_index, dst_y_index, code=0):
        """
        checks for amount of pieces in between src and dst

        Returns:
            bool: return true if no troops at all in between or 1 enemy troop
        """
        dat = dt.now()
        # 0:00:00.003471
        # checks that the path is according to damka rules
        # if abs(dst_x_index-src_x_index) == abs(dst_y_index-src_y_index):
        # the amount of tiles between src and dest \ HEETEK = displacement
        abs_displacement = abs(dst_x_index-src_x_index)
        directions = [(x, y) for x in range(-7, 8, 1)
                      for y in range(-7, 8, 1) if abs(x) == abs(y)]

        # constains the troops between the two locations
        in_between_troop_locs = \
            list({(x, y)
                  # Explantaion: for i in range(x_src+(1/-1),dst,(-1/1 - direction of moving))
                  for x in range(src_x_index+int((dst_x_index-src_x_index)/abs_displacement),
                                 dst_x_index, int((dst_x_index-src_x_index)/abs_displacement))
                  for y in range(src_y_index+int((dst_y_index-src_y_index)/abs_displacement),
                                 dst_y_index, int((dst_y_index-src_y_index)/abs_displacement))
                  for dirc in directions
                  # checks if the location generated is abs with the location
                  if (x+dirc[0], y+dirc[1]) in [(src_x_index, src_y_index), (dst_x_index, dst_y_index)]
                  # checks location is a troop
                  and isinstance(self._current_troops_array[x][y], Troop)})

        print("after: ", in_between_troop_locs)
        print(len(in_between_troop_locs))
        print(dt.now() - dat)
        print(self)
        print(src_x_index, src_y_index)

        # code = 1 means were checking if we can eat and we need the cordinits of the to be eaten
        if code == 1:
            if len(in_between_troop_locs) == 0:
                return []
            elif len(in_between_troop_locs) == 1:
                if self._current_troops_array[in_between_troop_locs[0][0]][in_between_troop_locs[0][1]].color == self._current_troops_array[src_x_index][src_y_index].color:
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
                if self._current_troops_array[in_between_troop_locs[0][0]][in_between_troop_locs[0][1]].color == self._current_troops_array[src_x_index][src_y_index].color:
                    return False
                # and one enemy is good - the rest bad
                return True
            return False

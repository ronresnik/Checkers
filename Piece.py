"""[summary]

Raises:
    ValueError: [description]

Returns:
    [type]: [description]
"""
import os
import pygame
from copy import deepcopy
from constants import RANGE, TILE_WIDTH, BASE_DIR, RED_BASE, BLACK_BASE, RED, BLACK

RIGHT_EAT = ("{}+1", "{}-1*{}")
BACK_RIGHT_EAT = ("{}+1", "{}-1*-{}")
LEFT_EAT = ("{}-1", "{}-1*{}")
BACK_LEFT_EAT = ("{}-1", "{}-1*-{}")
LEFT_COL = 0
RIGHT_COL = 7


class Troop:
    """[summary]
    """

    def __init__(self, image, state, x, y, x_picture, y_picture, color):
        self.image = image
        self.state = state
        self.x = x
        self.y = y
        self.x_picture = x_picture
        self.y_picture = y_picture
        self.color = color

    def __repr__(self):
        return "1" if self.color == RED else "2"

    def set_new_cordinates(self, x, y, game):
        """[summary]

        """
        self.x = x
        self.y = y
        self.x_picture = (self.x * TILE_WIDTH) + 25
        self.y_picture = (self.y * TILE_WIDTH) + 25

        if (x, y) in RED_BASE and self.color == BLACK \
                or (x, y) in BLACK_BASE and self.color == RED:
            color_name = "Black" if self.color == BLACK else "Red"
            game.__dict__[f"{color_name.lower()}_queen_left"] += 1
            game.__dict__[f"{color_name.lower()}_left"] -= 1
            return Queen(*[self.__dict__[key]
                           for key in self.__dict__.keys() if key != "image"])
        return self

    def get_eat_locs(self, game, src_x, src_y, i, eat_move, color, prevoius):
        """[summary]

        Args:
            game ([type]): [description]
            src_x ([type]): [description]
            src_y ([type]): [description]
            i ([type]): [description]
            eat_move ([type]): [description]
            color ([type]): [description]
            prevoius ([type]): [description]

        Returns:
            [type]: [description]
        """
        eaten_x_string, eaten_y_string = eat_move
        eaten_x = int(eval(eaten_x_string.format(src_x)))
        eaten_y = int(eval(eaten_y_string.format(src_y, i)))
        eaten_x_string = eaten_x_string.replace('1', '2')
        eaten_y_string = eaten_y_string.replace('1', '2')
        dest_x = int(eval(eaten_x_string.format(src_x)))
        dest_y = int(eval(eaten_y_string.format(src_y, i)))
        if game.board.is_loc_free(dest_x, dest_y, prevoius) and isinstance(game.board[eaten_x, eaten_y], Troop) and game.board[eaten_x, eaten_y].color != color:
            return (True, eaten_x, eaten_y, dest_x, dest_y)
        return (False, eaten_x, eaten_y, dest_x, dest_y)

    def can_eat(self, game, possible_locs, color, prevoius, src_x, src_y, i, eat_move):
        """[summary]"""
        # try to get the etean locs and dest locs
        can_eat, eaten_x, eaten_y, dest_x, dest_y = self.get_eat_locs(
            game, src_x, src_y, i, eat_move, color, prevoius)
        # if successful
        if can_eat:
            possible_locs[(src_x, src_y, dest_x, dest_y)] = [
                (eaten_x, eaten_y)]
            self.moving_algorithem(dest_x, dest_y, True, game,
                                   possible_locs, color, prevoius=(src_x, src_y))

    def moving_algorithem(self, x, y, just_eat, game, possible_locs, color, prevoius=None):
        # Do not search for additional locs when you get crowned
        if ((x, y) in RED_BASE and color == BLACK) or ((x, y) in BLACK_BASE and color == RED):
            return possible_locs
        # in order to later check if possible locations were added
        #save_start = deepcopy(possible_locs)
        if self.color == RED:
            i = -1
        else:  # MUST self.color == BLACK
            i = 1
        if x == LEFT_COL:
            if not just_eat:
                possible_locs[(x, y, x+1, y-1*i)] = []
            # checks if self can eat RIGHT - is can - updates possible_locs
            self.can_eat(game, possible_locs, color, prevoius, x, y, i,
                         RIGHT_EAT)
        elif x == RIGHT_COL:
            if not just_eat:
                possible_locs[(x, y, x-1, y-1*i)] = []
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, LEFT_EAT)
        else:
            if not just_eat:
                possible_locs[(x, y, x - 1, y - 1*i)] = []
                possible_locs[(x, y, x + 1, y - 1*i)] = []

            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, LEFT_EAT)
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, RIGHT_EAT)

            if just_eat:
                self.can_eat(game, possible_locs, color, prevoius,
                             x, y, i, BACK_LEFT_EAT)
                self.can_eat(game, possible_locs, color, prevoius,
                             x, y, i, BACK_RIGHT_EAT)

        return possible_locs

    def get_valid_moves(self, game, can_advance=None, get_eaten=None):
        """ """
        #t0 = time.perf_counter()
        empty_dict = {}
        possible_locs = self.moving_algorithem(self.x, self.y, False, game,
                                               empty_dict, self.color)
        for _ in range(4):
            append_to_del = []
            y = {}
            starts_dests = possible_locs.keys()
            for tail in starts_dests:
                for head in starts_dests:
                    if (head[0], head[1]) == (tail[2], tail[3]):
                        y[(tail[0], tail[1], head[2], head[3])
                          ] = possible_locs[tail] + possible_locs[head]
                        append_to_del.append(head)
            possible_locs.update(y)
            for to_del in list(set(append_to_del)):
                del possible_locs[to_del]
        possible_locs_list = [(item[0][2], item[0][3]) for item in possible_locs.items()
                              if (item[0][2], item[0][3]) in RANGE
                              and game.board.is_loc_free(item[0][2], item[0][3])]
        possible_locs_dict = {(item[0][2], item[0][3]): possible_locs[item[0]] for item in possible_locs.items()
                              if (item[0][2], item[0][3]) in RANGE
                              and game.board.is_loc_free(item[0][2], item[0][3])}
        if can_advance:
            if (can_advance[0], can_advance[1]) in possible_locs_list:
                return True
            return False
        if get_eaten:
            return possible_locs_dict
        return possible_locs_list


class Queen(Troop):
    """[summary]

    Args:
        Troop ([type]): [description]
    """

    def __init__(self, state, x, y, x_picture, y_picture, color):
        picture_color = "Black" if color == BLACK else "Red"
        image = pygame.image.load(os.path.join(
            BASE_DIR, f"static\\images\\{picture_color}Queen.png"))
        super().__init__(image, state, x, y, x_picture, y_picture, color)

    def __repr__(self):
        return "-1" if self.color == RED else "-2"

    def set_new_cordinates(self, x, y, game):
        """[summary]

        """
        self.x = x
        self.y = y
        self.x_picture = (self.x * TILE_WIDTH) + 25
        self.y_picture = (self.y * TILE_WIDTH) + 25
        return self

    def moving_algorithem(self, x, y, just_eat, game, possible_locs, color, prevoius=None):

        #save_start = deepcopy(possible_locs)
        if self.color == RED:
            i = -1
        else:  # MUST self.color == BLACK
            i = 1
        if x == LEFT_COL:
            if not just_eat:
                possible_locs[(x, y, x+1, y-1*i)] = []
                possible_locs[(x, y, x+1, y-1*-i)] = []
            # if the dest is free and in between ia a enemy Troop - Than I'ts OK for eating
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, RIGHT_EAT)
        elif x == RIGHT_COL:
            if not just_eat:
                possible_locs[(x, y, x-1, y-1*i)] = []
                possible_locs[(x, y, x-1, y-1*-i)] = []
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, LEFT_EAT)
        else:
            if not just_eat:
                possible_locs[(x, y, x - 1, y - 1*i)] = []
                possible_locs[(x, y, x + 1, y - 1*i)] = []
                possible_locs[(x, y, x - 1, y - 1*-i)] = []
                possible_locs[(x, y, x + 1, y - 1*-i)] = []

            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, LEFT_EAT)
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, RIGHT_EAT)
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, BACK_LEFT_EAT)
            self.can_eat(game, possible_locs, color,
                         prevoius, x, y, i, BACK_RIGHT_EAT)

        # # If no possible locations are found
        # if possible_locs == save_start:
        #     empty = {}
        #     # Then update with nothing in order to finish the recursion pattern
        #     return possible_locs.update(empty)
        return possible_locs

    def get_valid_moves(self, game, can_advance=None, get_eaten=None):
        """ """
        #t0 = time.perf_counter()
        empty_dict = {}
        possible_locs = self.moving_algorithem(self.x, self.y, False, game,
                                               empty_dict, self.color)
        for _ in range(4):
            append_to_del = []
            y = {}
            starts_dests = possible_locs.keys()
            for tail in starts_dests:
                for head in starts_dests:
                    if (head[0], head[1]) == (tail[2], tail[3]):
                        y[(tail[0], tail[1], head[2], head[3])
                          ] = possible_locs[tail] + possible_locs[head]
                        append_to_del.append(head)
            possible_locs.update(y)
            for to_del in list(set(append_to_del)):
                del possible_locs[to_del]
        possible_locs_list = [(item[0][2], item[0][3]) for item in possible_locs.items()
                              if (item[0][2], item[0][3]) in RANGE
                              and game.board.is_loc_free(item[0][2], item[0][3])]
        possible_locs_dict = {(item[0][2], item[0][3]): possible_locs[item[0]] for item in possible_locs.items()
                              if (item[0][2], item[0][3]) in RANGE
                              and game.board.is_loc_free(item[0][2], item[0][3])}
        if can_advance:
            if (can_advance[0], can_advance[1]) in possible_locs_list:
                return True
            return False
        if get_eaten:
            return possible_locs_dict
        return possible_locs_list

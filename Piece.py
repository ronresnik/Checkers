"""[summary]

Raises:
    ValueError: [description]

Returns:
    [type]: [description]
"""
import os
import pygame
from constants import RANGE, TILE_WIDTH, BASE_DIR, WHITE_BASE, BLACK_BASE


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
        return "1" if self.color == "Red" else "2"

    def set_new_cordinates(self, x, y):
        """[summary]

        """
        self.x = x
        self.y = y
        self.x_picture = (self.x * TILE_WIDTH) + 25
        self.y_picture = (self.y * TILE_WIDTH) + 25

        if (x, y) in WHITE_BASE and self.color == "Black" \
                or (x, y) in BLACK_BASE and self.color == "Red":
            return Queen(*[self.__dict__[key]
                           for key in self.__dict__.keys() if key != "image"])
        return self

    def can_eat(self, game_board, get_locs=False):
        "possible locations"
        locs = []
        for loc in [(self.x+i*2, self.y+j*2, self.x+i, self.y+j)
                    for i in range(-1, 2, 2) for j in range(-1, 2, 2)
                    if (self.x+i*2, self.y+j*2) in RANGE
                    and (self.x+i, self.y+j) in RANGE]:
            if game_board.is_loc_free(loc[0], loc[1]) \
                    and isinstance(game_board[loc[2], loc[3]], Troop) \
                    and game_board[loc[2], loc[3]].color != self.color:
                if get_locs:
                    locs.append(loc)
                else:
                    return True
        if get_locs:
            return locs
        return False

    def can_advance(self, dst_x, dst_y, game, just_eat=False, get_locs=False):
        """ """
        if not game.it_is_this_color_turn(self):
            return False
        # distinguish between simple moving and eating with moving
        possible_loc1 = None
        possible_loc2 = None
        eat_loc1 = None
        eat_loc2 = None
        if self.color == "Red":

            if self.x == 7:
                possible_loc1 = (self.x-1, self.y+1)
                eat_loc1 = (self.x-2, self.y+2)
            elif self.x == 0:
                possible_loc1 = (self.x+1, self.y+1)
                eat_loc1 = (self.x+2, self.y+2)
            else:
                possible_loc1 = (self.x-1, self.y + 1)
                possible_loc2 = (self.x+1, self.y + 1)
                eat_loc1 = (self.x-2, self.y + 2)
                eat_loc2 = (self.x+2, self.y + 2)

        else:  # MUST self.color == "Black"

            if self.x == 0:
                possible_loc1 = (self.x+1, self.y-1)
                eat_loc1 = (self.x+2, self.y-2)
            elif self.x == 7:
                possible_loc1 = (self.x-1, self.y-1)
                eat_loc1 = (self.x-2, self.y-2)
            else:
                possible_loc1 = (self.x - 1, self.y - 1)
                possible_loc2 = (self.x + 1, self.y - 1)
                eat_loc1 = (self.x - 2, self.y - 2)
                eat_loc2 = (self.x + 2, self.y - 2)
        try:
            eaten_x, eaten_y = game.board.get_in_between_cordinates(
                self.x, self.y, dst_x, dst_y)
            if(isinstance(game.board[eaten_x, eaten_y], Troop)
                    and game.board[eaten_x, eaten_y].color != self.color):
                possible_locs = [possible_loc1,
                                 possible_loc2, eat_loc1, eat_loc2]
            else:
                raise ValueError
        except ValueError:
            possible_locs = [possible_loc1, possible_loc2]
        if just_eat:
            for loc in self.can_eat(game.board, get_locs=True):
                possible_locs.append((loc[0], loc[1]))
        possible_locs = [loc for loc in possible_locs if loc is not None and loc in RANGE
                         and game.board.is_loc_free(loc[0], loc[1])]
        print("possible advancing locations", possible_locs)
        if get_locs:
            return possible_locs
        if (dst_x, dst_y) in possible_locs:
            return True
        return False


class Queen(Troop):
    """[summary]

    Args:
        Troop ([type]): [description]
    """

    def __init__(self, state, x, y, x_picture, y_picture, color):
        image = pygame.image.load(os.path.join(
            BASE_DIR, f"static\\images\\{color}Queen.png"))
        super().__init__(image, state, x, y, x_picture, y_picture, color)

    def __repr__(self):
        return "-1" if self.color == "Red" else "-2"

    # TODO - document can_eat

    def can_eat(self, game_board, get_locs=False):
        possible_locs = [(self.x+i, self.y+j) for j in range(-10, 10) for i in range(-10, 10)
                         if abs(i) == abs(j) and (self.x+i, self.y+j) in RANGE
                         and ((self.x+i, self.y+j) != (self.x, self.y))
                         and game_board.is_loc_free(self.x+i, self.y+j)
                         and len(game_board.is_only_one_enemy_in_between(self.x, self.y, self.x+i, self.y+j, 1)) == 1]
        print("possible eat locations", possible_locs)
        if get_locs:
            return possible_locs
        if len(possible_locs) >= 1:
            return True
        return False

    # TODO - document can_advance
    def can_advance(self, dst_x, dst_y, game, just_eat=False, get_locs=False):
        if not game.it_is_this_color_turn(self):
            return False
        # distinguish between simple moving and eating with moving
        possible_locs = [(self.x+i, self.y+j) for j in range(-10, 10) for i in range(-10, 10)
                         if abs(i) == abs(j) and (self.x+i, self.y+j) in RANGE
                         and ((self.x+i, self.y+j) != (self.x, self.y))
                         and game.board.is_loc_free(self.x+i, self.y+j)
                         and game.board.is_only_one_enemy_in_between(self.x, self.y, self.x+i, self.y+j)]
        print("possible advancing locations", possible_locs)
        if just_eat:
            possible_locs += self.can_eat(game.board, get_locs=True)
        if get_locs:
            return possible_locs
        if (dst_x, dst_y) in possible_locs:
            return True
        return False

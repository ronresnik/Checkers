"""[summary]

Raises:
    ValueError: [description]

Returns:
    [type]: [description]
"""
import os
import pygame
# Set color with rgb
white, black, red = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Beginning of logic
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Beginning of logic
BASE_DIR = os.path.dirname(__file__)
GAME_EXIT = False
PIECES_IN_ROW = 8
TILES_IN_ROW = 8
PIECES_IN_COLLUMN = 3
TILE_WIDTH = 100
RADIUS = 25
RANGE = [(x, y) for x in range(8) for y in range(8)]


class Troop:
    """[summary]
    """

    def __init__(self, image, state, x_index, y_index, x_picture, y_picture, color):
        self.image = image
        self.state = state
        self.x_index = x_index
        self.y_index = y_index
        self.x_picture = x_picture
        self.y_picture = y_picture
        self.color = color

    def __repr__(self):
        return "1" if self.color == "Red" else "2"

    def can_eat(self, game_board, get_locs=False):
        "possible locations"
        locs = []
        for loc in [(self.x_index+i*2, self.y_index+j*2, self.x_index+i, self.y_index+j)
                    for i in range(-1, 2, 2) for j in range(-1, 2, 2)
                    if (self.x_index+i*2, self.y_index+j*2) in RANGE
                    and (self.x_index+i, self.y_index+j) in RANGE]:
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

    def set_new_cordinates(self, x_index, y_index):
        """[summary]

        Args:
            x_index ([type]): [description]
            y_index ([type]): [description]
        """
        self.x_index = x_index
        self.y_index = y_index
        self.x_picture = (self.x_index * TILE_WIDTH) + 25
        self.y_picture = (self.y_index * TILE_WIDTH) + 25

    def can_advance(self, dst_x_index, dst_y_index, game_board, just_eat=False):
        """[summary]

        Args:
            dst_x_index ([type]): [description]
            dst_y_index ([type]): [description]
            game_board ([type]): [description]

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        # distinguish between simple moving and eating with moving
        possible_loc1 = None
        possible_loc2 = None
        eat_loc1 = None
        eat_loc2 = None
        if self.color == "Red":

            if self.x_index == 7:
                possible_loc1 = (self.x_index-1, self.y_index+1)
                eat_loc1 = (self.x_index-2, self.y_index+2)
            elif self.x_index == 0:
                possible_loc1 = (self.x_index+1, self.y_index+1)
                eat_loc1 = (self.x_index+2, self.y_index+2)
            else:
                possible_loc1 = (self.x_index-1, self.y_index + 1)
                possible_loc2 = (self.x_index+1, self.y_index + 1)
                eat_loc1 = (self.x_index-2, self.y_index + 2)
                eat_loc2 = (self.x_index+2, self.y_index + 2)

        else:  # MUST self.color == "Black"

            if self.x_index == 0:
                possible_loc1 = (self.x_index+1, self.y_index-1)
                eat_loc1 = (self.x_index+2, self.y_index-2)
            elif self.x_index == 7:
                possible_loc1 = (self.x_index-1, self.y_index-1)
                eat_loc1 = (self.x_index-2, self.y_index-2)
            else:
                possible_loc1 = (self.x_index - 1, self.y_index - 1)
                possible_loc2 = (self.x_index + 1, self.y_index - 1)
                eat_loc1 = (self.x_index - 2, self.y_index - 2)
                eat_loc2 = (self.x_index + 2, self.y_index - 2)

        try:
            eaten_x_index, eaten_y_index = game_board.get_in_between_cordinates(
                self.x_index, self.y_index, dst_x_index, dst_y_index)
            if(isinstance(game_board[eaten_x_index, eaten_y_index], Troop)
                    and game_board[eaten_x_index, eaten_y_index].color != self.color):
                possible_locs = [possible_loc1,
                                 possible_loc2, eat_loc1, eat_loc2]
            else:
                print("IN THIS RAREEDFCVJ DSFJKS")
                raise ValueError
        except ValueError:
            possible_locs = [possible_loc1, possible_loc2]
        if just_eat:
            for loc in self.can_eat(game_board, True):
                possible_locs.append((loc[0], loc[1]))
        possible_locs = [loc for loc in possible_locs if loc is not None and loc in RANGE
                         and game_board.is_loc_free(loc[0], loc[1])]
        print("possible advancing locations", possible_locs)
        if (dst_x_index, dst_y_index) in possible_locs:
            return True
        return False
    # def get_possible_moves(self):
    #     get_current_troops_positions()
    #     return possible_moves
    # def move_to(self):
    #
    #     # make the borad with proper index with letters and numbers
    #     # than moving the piece will be as easy as deletig it and reposting it at
    #     # diffrent location
    #


class Queen(Troop):
    """[summary]

    Args:
        Troop ([type]): [description]
    """

    def __init__(self, state, x_index, y_index, x_picture, y_picture, color):
        image = pygame.image.load(os.path.join(
            BASE_DIR, f"static\\images\\{color}Queen.png"))
        super().__init__(image, state, x_index, y_index, x_picture, y_picture, color)

    def __repr__(self):
        return "-1" if self.color == "Red" else "-2"

    # TODO - document can_eat

    def can_eat(self, game_board):
        possible_locs = [(self.x_index+i, self.y_index+j) for j in range(-10, 10) for i in range(-10, 10)
                         if abs(i) == abs(j) and (self.x_index+i, self.y_index+j) in RANGE
                         and ((self.x_index+i, self.y_index+j) != (self.x_index, self.y_index))
                         and game_board.is_loc_free(self.x_index+i, self.y_index+j)
                         and len(game_board.is_only_one_enemy_in_between(self.x_index, self.y_index, self.x_index+i, self.y_index+j, 1)) == 1]
        print("possible eat locations", possible_locs)
        if len(possible_locs) >= 1:
            return True
        return False

    # TODO - document can_advance
    def can_advance(self, dst_x_index, dst_y_index, game_board, code=0):
        """[summary]

        Args:
            dst_x_index ([type]): [description]
            dst_y_index ([type]): [description]
            game_board ([type]): [description]

        Returns:
            [type]: [description]
        """
        # distinguish between simple moving and eating with moving
        possible_locs = [(self.x_index+i, self.y_index+j) for j in range(-10, 10) for i in range(-10, 10)
                         if abs(i) == abs(j) and (self.x_index+i, self.y_index+j) in RANGE
                         and ((self.x_index+i, self.y_index+j) != (self.x_index, self.y_index))
                         and game_board.is_loc_free(self.x_index+i, self.y_index+j)
                         and game_board.is_only_one_enemy_in_between(self.x_index, self.y_index, self.x_index+i, self.y_index+j)]
        print("possible advancing locations", possible_locs)
        if code == "eat":
            return possible_locs
        if (dst_x_index, dst_y_index) in possible_locs:
            return True
        return False


def get_index(x_dest, y_dest):
    """[summary]

    Args:
        x_dest ([type]): [description]
        y_dest ([type]): [description]

    Returns:
        [type]: [description]
    """
    return int(x_dest/100), int(y_dest/100)

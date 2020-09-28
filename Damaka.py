"""
"""
import os
import pygame
from collections import deque
from Board import Board
from Piece import Troop, Queen, get_index


# FPS = 60 # frames per second setting

# set color with rgb
WHITE, BLACK, RED = (255, 255, 255), (0, 0, 0), (255, 0, 0)

# Beginning of logic
BASE_DIR = os.path.dirname(__file__)
GAME_EXIT = False
EAT = False  # Explantaion:
PIECES_IN_ROW = 8
TILES_IN_ROW = 8
PIECES_IN_COLLUMN = 3
TILE_WIDTH = 100
RADIUS = 25
WHITE_BASE = [(i, 0) for i in range(8)]
BLACK_BASE = [(i, 7) for i in range(8)]
"""
 inital_troops_array= \
                    [[1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [1,1,1,1,1,1,1,1],
                    [0,0,0,0,0,0,0,0],
                    [0,0,0,0,0,0,0,0],
                    [2,2,2,2,2,2,2,2],
                    [2,2,2,2,2,2,2,2],
                    [2,2,2,2,2,2,2,2]]
"""


def try_to_eat(src_x_index, src_y_index, dst_x_index, dst_y_index, game_board):
    try:
        eaten_x_index, eaten_y_index = game_board.get_in_between_cordinates(
            src_x_index, src_y_index, dst_x_index, dst_y_index)
        if(isinstance(game_board[eaten_x_index, eaten_y_index], Troop)
                and game_board[eaten_x_index, eaten_y_index].color != temp_piece.color):
            game_board[eaten_x_index, eaten_y_index] = 0
            print(
                f"Troop in index: {eaten_x_index},{eaten_y_index} was just eaten")
            return True

    except ValueError:
        print("Simple advancment move preformed")
        return False

    except IndexError:
        print("multiple tiles move")
        return False


def save_current_board(undo_stack, game_board, temp_piece, src_x_index, src_y_index):
    """[summary]

    Args:
        undo_stack ([type]): [description]
        game_board ([type]): [description]
        src_x_index ([type]): [description]
        src_y_index ([type]): [description]
    """
    try:
        undo_board = game_board.to_list(src_x_index, src_y_index)
        undo_stack.append(undo_board)
        # EAT = False
        temp_piece.set_new_cordinates(dst_x_index, dst_y_index)
        return True
    except Exception as e:
        return False


def change_player(game_board, src_x_index, src_y_index, dst_x_index, dst_y_index, temp_piece, EAT):
    # NOW WE HAVE ONLY MULTIPLE EATING SARUF saruf_check
    # TODO NotImplemented - simple move - could eat
    if game_board.has_SARUF_suspicous \
            and game_board.suspicous_could_eat(src_x_index, src_y_index) and not EAT:  # or didnt eat and could eat - pass color
        print(
            f"SARUF! - {game_board.SARUF_suspicous_x},{game_board.SARUF_suspicous_y} could eat again ()but you didn't")
        game_board[game_board.SARUF_suspicous_x,
                   game_board.SARUF_suspicous_y] = 0

        game_board.update_turn()

    elif (EAT and game_board[dst_x_index, dst_y_index].can_eat(game_board)):
        print("You can play again")
        game_board.set_SARUF_suspicous(
            dst_x_index, dst_y_index)
    else:
        print(f"Color {temp_piece.color} Turn Ended.")
        game_board.has_SARUF_suspicous = False
        game_board.update_turn()

    temp_piece = None


def try_to_asscend(temp_piece):
    if (temp_piece.x_index, temp_piece.y_index) in WHITE_BASE and temp_piece.color == "Black" \
            or (temp_piece.x_index, temp_piece.y_index) in BLACK_BASE and temp_piece.color == "Red":
        return Queen(*[temp_piece.__dict__[key] for key in temp_piece.__dict__.keys() if key != "image"])
    return temp_piece


def update_game(game_board, temp_piece, src_x_index, src_y_index):
    game_board[src_x_index, src_y_index] = 0
    temp_piece.state = True
    game_board[dst_x_index, dst_y_index] = temp_piece
    print("END")


def try_to_get_piece(game_board, x_index,  y_index):
    try:
        temp_piece = game_board[x_index, y_index]
        if game_board.it_is_this_color_turn(temp_piece):
            game_board[temp_piece.x_index, temp_piece.y_index].state = False
            return temp_piece

    except AttributeError:
        print("Please choose a tile contaning a piece")
        return 0


def piece_mousedown(game_board, x_index, y_index):
    temp_piece = try_to_get_piece(game_board, x_index, y_index)
    return temp_piece


def piece_mouseup(temp_piece, game_board, undo_stack):
    src_x_index, src_y_index = temp_piece.x_index, temp_piece.y_index
    save_current_board(undo_stack, game_board, temp_piece,
                       src_x_index, src_y_index)
    EAT = try_to_eat(src_x_index, src_y_index,
                     temp_piece.x_index, temp_piece.y_index, game_board)
    temp_piece = try_to_asscend(temp_piece)
    update_game(game_board, temp_piece, src_x_index, src_y_index,)
    # -----------------------END OF BASIC MOVE--------------------------------
    change_player(game_board, src_x_index, src_y_index,
                  temp_piece.x_index, temp_piece.y_index, temp_piece, EAT)
    print(game_board)


if __name__ == "__main__":
    print(BASE_DIR)
    # drawig the board
    pygame.init()
    game_board = Board()
    gg = Board()
    gg = game_board
    undo_stack = deque()
    while not GAME_EXIT:  # Main game loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                GAME_EXIT = True
            if event.type == pygame.MOUSEBUTTONDOWN:

                m_x, m_y = pygame.mouse.get_pos()
                print("\n~~~~~~MOUSEBUTTONDOWN~~~~~~~~")
                x_index, y_index = get_index(*pygame.mouse.get_pos())
                print(f"Source Board index: {x_index}, {y_index}")
                temp_piece = piece_mousedown(game_board, x_index, y_index)
            
            # i am adding this line to see if shit happens
            if event.type == pygame.MOUSEBUTTONUP:
                print("\n-------MOUSEBUTTONUP------")
                dst_x_index, dst_y_index = get_index(*pygame.mouse.get_pos())
                if isinstance(temp_piece, Troop) and game_board.it_is_this_color_turn(temp_piece) \
                        and temp_piece.can_advance(dst_x_index, dst_y_index, game_board, EAT):
                    print(
                        f"Destination Board index: {dst_x_index}, {dst_y_index} Color: {temp_piece.color}")
                    piece_mouseup(temp_piece, game_board, undo_stack)

                elif isinstance(temp_piece, int) or temp_piece is None:
                    # {non piece land}
                    print("idgaf!")
                else:
                    # {cannot advance}
                    temp_piece.state = True
                    game_board[temp_piece.x_index,
                               temp_piece.y_index] = temp_piece
                    print("The troop canot advance to the desired destanation")
                    temp_piece = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        # {retrive prevoius board}
                        game_board = Board(*undo_stack.pop())
                        game_board.draw_pieces()

    pygame.quit()
    quit()

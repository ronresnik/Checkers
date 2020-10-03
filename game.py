"""
"""
from collections import deque
import pygame
from board import Board
from piece import Troop, Queen
from constants import WHITE_BASE, BLACK_BASE, RED, GREY, WHITE, RED, TILE_WIDTH
# FPS = 60 # frames per second setting

# set color with rgb

# Beginning of logic
EAT = False  # Explantaion:

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


class Game():

    def __init__(self, board=None, undo_stack=deque(), __turn="Red"):
        if board == None:
            self.board = Board()
        else:
            self.board = Board(*board)
        self.undo_stack = undo_stack
        self.__turn = __turn

    def to_list(self, x, y):
        return [self.board.to_list(x, y), self.undo_stack, self.__turn]

    def change_turn(self, code=1):
        """[summary]
        """
        if self.__turn == "Red":
            self.__turn = "Black"
        else:
            self.__turn = "Red"

    def it_is_this_color_turn(self, piece):
        """[summary]

        Returns:
            [type]: [description]
        """
        return self.__turn == piece.color

    def try_to_eat(self, src_x, src_y, piece):

        dst_x, dst_y, color = piece.x, piece.y, piece.color
        global EAT
        try:
            eaten_x, eaten_y = self.board.get_in_between_cordinates(
                src_x, src_y, dst_x, dst_y)
            if(isinstance(self.board[eaten_x, eaten_y], Troop)
                    and self.board[eaten_x, eaten_y].color != color):
                self.board[eaten_x, eaten_y] = 0
                print(f"Troop in index: {eaten_x},{eaten_y} was just eaten")
                EAT = True

        except ValueError:
            print("Simple advancment move preformed")
            EAT = False

        except IndexError:
            print("multiple tiles move")
            EAT = False

    def save_game(self, piece):
        """[summary]
        """
        try:
            undo_game = self.to_list(
                piece.x, piece.y)
            self.undo_stack.append(undo_game)
            # EAT = False
            self.board.piece = piece
            return True
        except Exception as e:
            return False

    def change_player(self, src_x, src_y, piece):
        # NOW WE HAVE ONLY MULTIPLE EATING SARUF saruf_check
        # TODO NotImplemented - simple move - could eat
        global EAT
        dst_x, dst_y = piece.x, piece.y
        if self.board.has_SARUF_suspicous \
                and self.board.suspicous_could_eat(src_x, src_y) and not EAT:  # or didnt eat and could eat - pass color
            print(
                f"SARUF! - {self.board.SARUF_suspicous_x},{self.board.SARUF_suspicous_y} could eat again ()but you didn't")
            self.board[self.board.SARUF_suspicous_x,
                       self.board.SARUF_suspicous_y] = 0

            self.change_turn()

        elif (EAT and self.board[dst_x, dst_y].can_eat(self.board)):
            print("You can play again")
            self.board.set_SARUF_suspicous(
                dst_x, dst_y)
        else:
            print(f"Color {piece.color} Turn Ended.")
            self.board.has_SARUF_suspicous = False
            self.change_turn()

        self.board.piece = None

    def update_game(self, src_x, src_y, piece):
        self.board[src_x, src_y] = 0
        piece.state = True
        self.board[piece.x, piece.y] = piece
        print("END")

    def get_piece(self, x,  y):
        try:
            piece = self.board[x, y]
            if self.it_is_this_color_turn(piece):
                self.board[piece.x,
                           piece.y].state = False
                return piece

        except AttributeError:
            print("Please choose a tile contaning a piece")
            return 0

    def play(self, x, y):
        global EAT
        if self.board.piece:
            piece = self.board.piece
            if isinstance(piece, Troop) and piece.can_advance(x, y, self, EAT):

                src_x, src_y = piece.x, piece.y
                piece = piece.set_new_cordinates(x, y)

                self.try_to_eat(src_x, src_y, piece)
                self.update_game(src_x, src_y, piece)
                self.change_player(src_x, src_y, piece)

            elif isinstance(piece, int) or piece is None:
                # {non piece land}
                print("pls choose a tile containg a piece")
            else:
                # {cannot advance}
                piece.state = True
                self.board[piece.x,
                           piece.y] = piece
                print("The troop canot advance to the desired destination")
                self.board.piece = None
        else:
            piece = self.get_piece(x, y)
            if isinstance(piece, Troop):
                self.save_game(piece)
                self.board.draw_valid_moves(piece, self)

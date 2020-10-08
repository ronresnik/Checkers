"""
"""
from collections import deque
import pygame
from board import Board
from piece import Troop
from constants import RED, BLACK


class Game():

    def __init__(self, board=None, undo_stack=deque(), __turn=RED, red_left=12, black_left=12, red_queen_left=0, black_queen_left=0, winner=None):
        if board == None:
            self.board = Board()
        else:
            self.board = Board(*board)
        self.undo_stack = undo_stack
        self.__turn = __turn
        self.red_left = red_left
        self.black_left = black_left
        self.red_queen_left = red_queen_left
        self.black_queen_left = black_queen_left
        self.winner = winner

    def to_list(self, x, y):
        return [self.board.to_list(x, y), self.undo_stack, self.__turn, self.red_left, self.black_left, self.red_queen_left, self.black_queen_left, self.winner]

    def change_turn(self):
        """[summary]
        """
        self.winner = self.__turn
        if self.__turn == RED:
            self.__turn = BLACK
            color = "Black"
        else:
            self.__turn = RED
            color = "Red"
        if not (self.__dict__[f"{color.lower()}_left"] == 0 and self.__dict__[f"{color.lower()}_queen_left"] == 0):
            self.winner = None

    def it_is_this_color_turn(self, piece):
        """[summary]

        """
        return self.__turn == piece.color

    def remove_eaten(self, dst_x, dst_y, piece):
        """[summary]
        """
        eaten_pices = piece.get_valid_moves(self, get_eaten=True)
        if eaten_pices[(dst_x, dst_y)]:
            for piece_to_be_removed in eaten_pices[(dst_x, dst_y)]:
                self.board[piece_to_be_removed[0], piece_to_be_removed[1]] = 0

    def save_game(self, piece):
        """[summary]
        """
        try:
            undo_game = self.to_list(
                piece.x, piece.y)
            self.undo_stack.append(undo_game)
            self.board.piece = piece
            return True
        except Exception as e:
            return False

    def update_game(self, x, y, piece):
        """[summary]
        """
        self.board[piece.x, piece.y] = 0
        piece = piece.set_new_cordinates(x, y, self)
        piece.state = True
        self.board[piece.x, piece.y] = piece
        self.change_turn()
        self.board.piece = None
        # print("END")

    def get_piece(self, x,  y):
        """[summary]
        """
        try:
            piece = self.board[x, y]
            if self.it_is_this_color_turn(piece):
                self.board[piece.x,
                           piece.y].state = False
                return piece

        except AttributeError:
            print("Please choose a tile contaning a piece")
            return 0

    def play(self, x, y, code=None):
        """[summary]
        """
        if self.board.piece:
            piece = self.board.piece
            if piece.get_valid_moves(self, can_advance=(x, y)):
                self.remove_eaten(x, y, piece)
                self.update_game(x, y, piece)
                if code == "PLAYER":
                    self.board.draw_pieces()

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
                if code == "PLAYER":
                    self.board.draw_pieces()
        else:
            piece = self.get_piece(x, y)
            if isinstance(piece, Troop):
                self.save_game(piece)
                if code == "PLAYER":
                    self.board.draw_valid_moves(piece, self)

    # ---------------- AI ----------------------
    def evaluate(self):
        # evaluate red-black?
        return self.red_left - self.black_left + (self.red_queen_left * 0.5 - self.black_queen_left * 0.5)

    def get_all_moves_games(self, color):
        moves = []
        for piece in self.board.get_all_pieces(color):
            valid_moves = piece.get_valid_moves(self)
            for dest_move in valid_moves:
                new_game = self.simulate_move(piece, dest_move)
                moves.append(new_game)

        return moves

    def simulate_move(self, piece, dest_move):
        new_game = Game(*self.to_list(piece.x, piece.y))
        new_game.play(piece.x, piece.y, "AI")
        new_game.play(dest_move[0], dest_move[1], "AI")
        return new_game

"""
"""
import pygame
from board import Board
from game import Game

# FPS = 60 # frames per second setting

# set color with rgb

# Beginning of logic
GAME_EXIT = False

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


def get_board_position(x_dest, y_dest):
    """[summary]
    """
    return int(x_dest/100), int(y_dest/100)


if __name__ == "__main__":
    # drawig the board
    pygame.init()
    game = Game()
    while not GAME_EXIT:  # Main game loop
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                GAME_EXIT = True
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = get_board_position(*pygame.mouse.get_pos())
                game.play(x, y)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    mods = pygame.key.get_mods()
                    if mods & pygame.KMOD_CTRL:
                        # {retrive prevoius board}
                        if len(game.undo_stack) > 0:
                            game = Game(*game.undo_stack.pop())
                            game.board.draw_pieces()

    pygame.quit()
    quit()

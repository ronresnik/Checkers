"""
"""
import pygame
import time
from game import Game
from algorithm import minimax
from constants import RED
# Beginning of logic
GAME_EXIT = False


def get_board_position(x_dest, y_dest):
    """[summary]
    """
    return int(x_dest/100), int(y_dest/100)


if __name__ == "__main__":
    # drawig the board
    pygame.init()
    game = Game()
    game.board.draw_pieces()
    while not GAME_EXIT:  # Main game loop
        for event in pygame.event.get():

            if game.winner:
                print(f"Congartulations Player Color {game.winner} WON!!!")
                pygame.quit()
                break

            if game._Game__turn == RED:
                t0 = time.perf_counter()
                gg, new_game = minimax(game, 4, RED)
                print("TIME: ", time.perf_counter() - t0)
                game = new_game
                game.board.draw_pieces()

            if event.type == pygame.QUIT:
                GAME_EXIT = True
            if event.type == pygame.MOUSEBUTTONDOWN:

                x, y = get_board_position(*pygame.mouse.get_pos())
                game.play(x, y, "PLAYER")

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

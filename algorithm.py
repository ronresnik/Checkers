"""[summary]

    Returns:
        [type]: [description]
    """
from constants import RED, BLACK
max_player = RED


def minimax(game, depth, max_player):
    """[summary]"""
    if depth == 0 or game.winner != None:
        # print(game.evaluate(), game)
        return game.evaluate(), game

    if max_player:
        maxEval = float('-inf')
        best_move_game = None
        for move_games in game.get_all_moves_games(RED):
            evaluation = minimax(move_games, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move_game = move_games

        return maxEval, best_move_game
    else:
        minEval = float('inf')
        best_move_game = None
        for move_games in game.get_all_moves_games(BLACK):
            evaluation = minimax(move_games, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move_game = move_games

        return minEval, best_move_game

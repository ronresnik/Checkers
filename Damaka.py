import pygame
import math
import Board
import Piece
pygame.init()

#set color with rgb
white,black,red = (255,255,255),(0,0,0),(255,0,0)
# Beginning of logic
gameExit = False
lead_x = 20
lead_y = 20
pieces_in_row = 8
tiles_in_row = 8
pieces_in_collum = 3
tile_width = 100
RADIUS = 25
complicated_locs = [(7,0),(7,1),(7,2),(7,3),(7,4),(7,5),(7,6),(7,7)]
#draw a rectangle

# inital_troops_array= \
#                    [[1,1,1,1,1,1,1,1],
#                    [1,1,1,1,1,1,1,1],
#                    [1,1,1,1,1,1,1,1],
#                    [0,0,0,0,0,0,0,0],
#                    [0,0,0,0,0,0,0,0],
#                    [2,2,2,2,2,2,2,2],
#                    [2,2,2,2,2,2,2,2],
#                    [2,2,2,2,2,2,2,2]]


#
# def get_current_troops_positions():
#     return updated_board
#
# def update_troops_position(troop_curr_loc, troop_future_loc):

if __name__ == "__main__":

    # drawig the board
    game_board = Board.Board()
    pygame.display.update()
    temp_piece = None
    while not gameExit:
        current_troops_array = game_board.get_current_troops_array()
        for event in pygame.event.get():
            pygame.display.update()
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                m_x, m_y = pygame.mouse.get_pos()
                for collum in current_troops_array:
                    for piece in collum:
                        if type(piece) is Piece.Piece and piece.state:
                            dis = math.sqrt(( (piece.x_picture+25) - m_x) ** 2 + ( (piece.y_picture+25) - m_y) ** 2)
                            if dis < RADIUS:
                                print("here")
                                temp_piece = piece
                                current_troops_array[piece.x_index][piece.y_index] = 0
                                game_board.set_current_troops_array(current_troops_array)
                                game_board.draw_pieces()
                                game_board.print_current_troops_array()



            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = pygame.mouse.get_pos()
                print(temp_piece.x_index, temp_piece.y_index)
                if type(temp_piece) is Piece.Piece and temp_piece.state:
                    print(m_x, m_y)
                    if temp_piece.can_advance(m_x, m_y):
                        print("can advance")
                        current_troops_array[temp_piece.x_index][ temp_piece.y_index] = 0
                        x_index, y_index = Piece.get_index(m_x, m_y)
                        temp_piece.set_new_cordinates(x_index, y_index)
                        current_troops_array[x_index][y_index]=temp_piece
                        game_board.set_current_troops_array(current_troops_array)
                        game_board.draw_pieces()


    pygame.quit()
    quit()
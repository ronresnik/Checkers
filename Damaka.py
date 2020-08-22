import pygame
import math
pygame.init()

#set color with rgb
white,black,red = (255,255,255),(0,0,0),(255,0,0)

#set display
gameDisplay = pygame.display.set_mode((800,800))

#caption
pygame.display.set_caption("Checkers")

#beginning of logic
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
gameDisplay.fill(white)
# inital_troops_array= \
#                    [[1,1,1,1,1,1,1,1],
#                    [1,1,1,1,1,1,1,1],
#                    [1,1,1,1,1,1,1,1],
#                    [0,0,0,0,0,0,0,0],
#                    [0,0,0,0,0,0,0,0],
#                    [2,2,2,2,2,2,2,2],
#                    [2,2,2,2,2,2,2,2],
#                    [2,2,2,2,2,2,2,2]]
class Piece:

    def __init__(self, image, state, x_index, y_index, x_picture, y_picture, color):
        self.image = image
        self.state = state
        self.x_index = x_index
        self.y_index = y_index
        self.x_picture = x_picture
        self.y_picture = y_picture
        self.color = color


    def set_new_cordinates(self, x_index, y_index):
        self.x_index = x_index
        self.y_index = y_index
        self.x_picture = (self.x_index * tile_width) + 25
        self.y_picture = (self.y_index * tile_width) + 25

    def set_state(self, state):
        self.state = state
    def can_advance(self, x_dest, y_dest):
        possible_loc1 = None
        possible_loc2 = None
        x_index, y_index = get_index(x_dest, y_dest)
        if (self.x_index, self.y_index) not in complicated_locs:
            if self.color == "White":
                if self.x_index == 0 and self.y_index !=0:
                    possible_loc1 = (1,self.y_index-1)
                    possible_loc2 = (1, self.y_index + 1)
                elif self.x_index != 0 and self.y_index ==0:
                    possible_loc1 = (self.x_index+1, 1)
                elif self.x_index == 0 and self.y_index ==0:
                    possible_loc1 = (1, 1)
                else:
                    possible_loc1 = (self.x_index-1, self.y_index + 1)
                    possible_loc2 = (self.x_index+1, self.y_index + 1)
                # then
                #  |
                #  |
                #  |
                # \ /
                #  .
            # else:
            #     if self.x_index == 0 and self.y_index !=0:
            #     elif self.x_index == 0 and self.y_index ==0:
            #     elif self.x_index == 0 and self.y_index ==0:
            #     else:
            #     # then
            #     #  .
            #     # / \
            #     #  |
            #     #  |
            #     #  |
            print(possible_loc1, possible_loc2)
            if (x_index, y_index) == possible_loc1 or (x_index, y_index) == possible_loc2:
                return True
        else:
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


def get_index( x_dest, y_dest):
    return  5, 3

#
# def get_current_troops_positions():
#     return updated_board
#
# def update_troops_position(troop_curr_loc, troop_future_loc):
class Board:


    def __init__(self):
        self.draw_board(tiles_in_row)
        self.current_troops_array = None
        self.initial_troops_array = None


    def create_initial_troops_pos(self):
        rows, cols = (8, 8)
        initial_troops_array = [[0 for i in range(cols)] for j in range(rows)]
        for x_index in range(pieces_in_row):
            # upper troops
            for y_index in range(pieces_in_collum):
                piece = Piece(pygame.image.load(r"P:\Users\ronre\Documents\ComputerScienceDocs\ChatApp\WhiteRegular.png"), True, x_index, y_index, (x_index * tile_width) + 25,
                            (y_index * tile_width) + 25, "White")
                initial_troops_array[x_index][y_index] = piece
                print(f"gg{type(piece)}gg")
            # lower troops
            for y_index in range(pieces_in_collum):
                piece = Piece(pygame.image.load(r"P:\Users\ronre\Documents\ComputerScienceDocs\ChatApp\BlackRegular.png"), True, x_index, y_index, (x_index * tile_width) + 25,
                            ((y_index+5) * tile_width) + 25, "Black")
                initial_troops_array[x_index][y_index+5] = piece
                #gameDisplay.blit(piece, ((x_index * tile_width) + 25, ((y_index + 5) * tile_width) + 25))
        self.initial_troops_array = initial_troops_array
        self.current_troops_array = initial_troops_array
        return initial_troops_array

    def set_current_troops_array(self, current_troops_array):
        self.current_troops_array = current_troops_array

    def get_current_troops_array(self):
        return self.current_troops_array

    def draw_pieces(self):
        gameDisplay.fill(white)
        self.draw_board(8)
        for collum in self.current_troops_array:
            for piece in collum:
                if type(piece) is Piece and piece.state:
                    gameDisplay.blit(piece.image, (piece.x_picture, piece.y_picture))
        pygame.display.update()


    def print_current_troops_array(self):
        rows, cols = (8, 8)
        matrix = [[0 for i in range(cols)] for j in range(rows)]
        for x_index in range(pieces_in_row):
            for y_index in range(pieces_in_collum):
                piece=self.current_troops_array[x_index][y_index]
                if type(piece) is Piece and piece.state:
                    matrix[x_index][y_index] = 1
                else:
                    matrix[x_index][y_index] = 0
        for collum in matrix:
            print(collum)

    def draw_board(self, tiles_in_row):
        for x_index in range(tiles_in_row):
            for y_index in range(tiles_in_row):
                if (x_index%2 ==0 and y_index%2!=0) or (x_index%2!=0 and y_index%2==0):
                    print("im here")
                    pygame.draw.rect(gameDisplay, black, [(x_index*100), (y_index*100), 100, 100])
        pygame.display.update()


    

if __name__ == "__main__":

    # drawig the board
    game_board = Board()
    initial_troops_array = game_board.create_initial_troops_pos()
    print(initial_troops_array)
    game_board.draw_pieces()
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
                        if type(piece) is Piece and piece.state:
                            dis = math.sqrt(( (piece.x_picture+25) - m_x) ** 2 + ( (piece.y_picture+25) - m_y) ** 2)
                            if dis < RADIUS:
                                temp_piece = piece
                                current_troops_array[piece.x_index][piece.y_index] = 0
                                game_board.set_current_troops_array(current_troops_array)
                                game_board.draw_pieces()
                                game_board.print_current_troops_array()



            if event.type == pygame.MOUSEBUTTONUP:
                m_x, m_y = pygame.mouse.get_pos()
                print(temp_piece.x_index, temp_piece.y_index)
                if type(temp_piece) is Piece and temp_piece.state:
                    print(m_x, m_y)
                    if temp_piece.can_advance(m_x, m_y):
                        print("can advance")
                        current_troops_array[temp_piece.x_index][ temp_piece.y_index] = 0
                        x_index, y_index = get_index(m_x, m_y)
                        temp_piece.set_new_cordinates(x_index, y_index)
                        current_troops_array[x_index][y_index]=temp_piece
                        game_board.set_current_troops_array(current_troops_array)
                        game_board.draw_pieces()

        #draw_pieces(current_troops_array)

    #quit from pygame & python
    pygame.quit()
    quit()
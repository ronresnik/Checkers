import Piece
import pygame

#set color with rgb
white,black,red = (255,255,255),(0,0,0),(255,0,0)



#beginning of logic
gameExit = False

lead_x = 20
lead_y = 20
pieces_in_row = 8
TILES_IN_ROW = 8
pieces_in_collum = 3
TILE_WIDTH = 100
RADIUS = 25
#draw a rectangle

class Board:
    __turn_counter = 0
    def __init__(self):
        self.under_cover_x = 0
        self.under_cover_y = 0
        self.is_under_cover = False
        # set display
        self.gameDisplay = pygame.display.set_mode((800, 800))

        # caption
        pygame.display.set_caption("Checkers")
        self.gameDisplay.fill(white)

        self.draw_board()
        self.initial_troops_array = self.create_initial_troops_pos()
        self.current_troops_array = self.initial_troops_array
        self.draw_pieces()

    def create_initial_troops_pos(self):
        rows, cols = (8, 8)
        initial_troops_array = [[0 for i in range(cols)] for j in range(rows)]
        for x_index in range(pieces_in_row):
            # upper troops
            for y_index in range(pieces_in_collum):
                piece = Piece.Piece(pygame.image.load(r"P:\Users\ronre\Documents\ComputerScienceDocs\Checkers\WhiteRegular.png"), True, x_index, y_index, (x_index * TILE_WIDTH) + 25,
                            (y_index * TILE_WIDTH) + 25, "White")
                initial_troops_array[x_index][y_index] = piece
            # lower troops
            for y_index in range(pieces_in_collum):
                piece = Piece.Piece(pygame.image.load(r"P:\Users\ronre\Documents\ComputerScienceDocs\Checkers\BlackRegular.png"), True, x_index, y_index+5, (x_index * TILE_WIDTH) + 25,
                            ((y_index+5) * TILE_WIDTH) + 25, "Black")
                initial_troops_array[x_index][y_index+5] = piece
                #gameDisplay.blit(piece, ((x_index * tile_width) + 25, ((y_index + 5) * tile_width) + 25))
        return initial_troops_array

    def set_current_troops_array(self, current_troops_array):
        self.current_troops_array = current_troops_array

    def get_current_troops_array(self):
        return self.current_troops_array

    def draw_pieces(self):
        self.gameDisplay.fill(white)
        self.draw_board()
        for column in self.current_troops_array:
            for piece in column:
                if type(piece) is Piece.Piece and piece.state:
                    self.gameDisplay.blit(piece.image, (piece.x_picture, piece.y_picture))
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

    def is_loc_free(self, x_dest, y_dest,  color_start):
        if type(self.current_troops_array[x_dest][y_dest]) is Piece and self.current_troops_array[x_dest][y_dest].color == color_start:
            print(x_dest, y_dest, "is taken")
            return False
        return True

    def update_turn(self):
        self.__turn_counter += 1
        print(self.__turn_counter)
    def draw_board(self):
        for x_index in range(TILES_IN_ROW):
            for y_index in range(TILES_IN_ROW):
                if (x_index % 2 == 0 and y_index % 2 != 0) or (x_index % 2 != 0 and y_index % 2 == 0):
                    pygame.draw.rect(self.gameDisplay, black, [(x_index*TILE_WIDTH), (y_index*TILE_WIDTH), TILE_WIDTH, TILE_WIDTH])
        pygame.display.update()

    def it_is_this_color_turn(self, piece):
        if (self.__turn_counter %2 == 0 and piece.color == "White") or (self.__turn_counter %2 != 0 and piece.color == "Black") :
            print(self.__turn_counter,piece.color)
            return True
        return False

    def set_under_cover(self, x_index, y_index):
        self.under_cover_x = x_index
        self.under_cover_y = y_index
        self.is_under_cover = True

    def piece_remained(self, x_index, y_index):
        if(self.under_cover_x, self.under_cover_y) != (x_index, y_index):
            self.is_under_cover = False
            return True
        return False

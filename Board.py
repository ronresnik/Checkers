import Piece
import pygame

#set color with rgb
white,black,red = (255,255,255),(0,0,0),(255,0,0)



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


class Board:

    def __init__(self):
        # set display
        self.gameDisplay = pygame.display.set_mode((800, 800))

        # caption
        pygame.display.set_caption("Checkers")
        self.gameDisplay.fill(white)

        self.draw_board(tiles_in_row)
        self.initial_troops_array = self.create_initial_troops_pos()
        self.current_troops_array = self.initial_troops_array
        self.draw_pieces()

    def create_initial_troops_pos(self):
        rows, cols = (8, 8)
        initial_troops_array = [[0 for i in range(cols)] for j in range(rows)]
        for x_index in range(pieces_in_row):
            # upper troops
            for y_index in range(pieces_in_collum):
                piece = Piece.Piece(pygame.image.load(r"P:\Users\ronre\Documents\ComputerScienceDocs\Checkers\WhiteRegular.png"), True, x_index, y_index, (x_index * tile_width) + 25,
                            (y_index * tile_width) + 25, "White")
                initial_troops_array[x_index][y_index] = piece
            # lower troops
            for y_index in range(pieces_in_collum):
                piece = Piece.Piece(pygame.image.load(r"P:\Users\ronre\Documents\ComputerScienceDocs\Checkers\BlackRegular.png"), True, x_index, y_index, (x_index * tile_width) + 25,
                            ((y_index+5) * tile_width) + 25, "Black")
                initial_troops_array[x_index][y_index+5] = piece
                #gameDisplay.blit(piece, ((x_index * tile_width) + 25, ((y_index + 5) * tile_width) + 25))
        return initial_troops_array

    def set_current_troops_array(self, current_troops_array):
        self.current_troops_array = current_troops_array

    def get_current_troops_array(self):
        return self.current_troops_array

    def draw_pieces(self):
        self.gameDisplay.fill(white)
        self.draw_board(8)
        for collum in self.current_troops_array:
            for piece in collum:
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

    def draw_board(self, tiles_in_row):
        for x_index in range(tiles_in_row):
            for y_index in range(tiles_in_row):
                if (x_index%2 ==0 and y_index%2!=0) or (x_index%2!=0 and y_index%2==0):
                    print("im here")
                    pygame.draw.rect(self.gameDisplay, black, [(x_index*100), (y_index*100), 100, 100])
        pygame.display.update()

# Set color with rgb
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
        print(x_index, y_index)
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


def get_index(x_dest, y_dest):
    return  int(x_dest/100), int(y_dest/100)
   #
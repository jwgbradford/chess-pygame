import pygame, math, sys, itertools, re, os, time
from pygame.math import Vector2

class Board():
    def __init__(self):
        # initalise pygame to start everything
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        pygame.display.set_caption('Chess')
        self.background = self.make_background()
        self.text_box = self.add_text_box(150, 30)
        self.player_turn = 0 # player 0 (white) goes first, then player 1 (black)

    def make_background(self): # this function creates a single image for the board squares and labels
        # set up a simple list of images that we can iterate through
        images = itertools.cycle((BLUE_IMAGE, GRAY_IMAGE))
        background = pygame.Surface((BOARD_SIZE, BOARD_SIZE))
        background.fill((255, 255, 255))
        # Use two nested for loops to get the coordinates.
        for row in range(TILES):
            for column in range(TILES):
                # This alternates between the blue and gray image.
                image = next(images)
                # Blit one image after the other at their respective coords
                background.blit(image, ((row * TILE_SIZE) + OFFSET, (column * TILE_SIZE) + OFFSET))
            next(images)
        background = self.mark_out(background)
        #returns a surface, ready to be sent to the screen
        return background

    def mark_out(self, background): # this function adds the column / row lables
        # position row labels
        for row, row_lable in enumerate(ROWS):
            txt_image = FONT.render(row_lable, True, (0, 0, 0))
            # labels up & down the left
            background.blit(txt_image, (5, (row * TILE_SIZE) + (OFFSET * 3)))
            # labels up and down the right, we use the same txt_image
            background.blit(txt_image, (BOARD_SIZE - 20, (row * TILE_SIZE) + (OFFSET * 3)))
        for column, column_lable in enumerate(COLUMNS):
            txt_image = FONT.render(column_lable, True, (0, 0, 0))
            # labels along the top
            background.blit(txt_image, ((column * TILE_SIZE) + (OFFSET * 3), 5))
            # labels along the bottom, we use the same txt_image
            background.blit(txt_image, ((column * TILE_SIZE) + (OFFSET * 3), BOARD_SIZE - 20))
        return background

    def load_pieces(self, file_name):
        input_file = open(PATH + file_name, 'r')
        input_data = input_file.readlines()
        input_file.closed

        input_split = []
        for entry in input_data:
            split_data = entry.split(', ')
            input_split.append(split_data)
        return input_split

    def add_pieces(self):
        pieces_list = self.load_pieces('default_board_layout.txt')
        # we place all our pieces in a group of sprites
        pieces_group = pygame.sprite.Group()
        # first create a blank board state
        board_state = []
        for column in range(0, TILES):
                columnlist = []
                for row in range(0, TILES):
                    columnlist.append(None)
                board_state.append(columnlist)
        # then read through our load list and swap in pieces
        for entry in pieces_list:
            piece_colour = entry[0]
            piece_name = entry[1]
            # because we're reading in from a file, we need to force python to treat as integer
            piece_index = int(entry[2])
            column = int(entry[3])
            row = int(entry[4])
            # we can use piece_index from our list of pieces to load separate class objects
            piece = ChessPiece(piece_name, piece_colour, column, row, pieces_group)
            board_state[column][row] = piece
            pieces_group.add(piece)
        return pieces_group, board_state

    def xy_to_board(self, pos):
        #first work out which row/column we clicked in
        column, row = pos
        column -= OFFSET
        row -= OFFSET
        if (column < 0 or row < 0 or
                column > (BOARD_SIZE - (OFFSET * 2)) or 
                row > (BOARD_SIZE - (OFFSET * 2))):
                return [99, 99]
        aligned_column = math.trunc(column / TILE_SIZE)
        aligned_row = math.trunc(row / TILE_SIZE)
        aligned_square = [aligned_column, aligned_row]
        return aligned_square

    def add_text_box(self, w, h): # creates the basic text input box
        self.BOX_COLOUR = pygame.Color('coral')
        temp_text_box = pygame.Surface((w, h))
        temp_text_box.fill(self.BOX_COLOUR)
        return temp_text_box

    def show_in_text_box(self, text):
        txt_surface = FONT.render(text, True, TEXT_COLOUR)
        self.text_box.fill(self.BOX_COLOUR)
        self.text_box.blit(txt_surface, (5, 5))
        self.screen.blit(self.text_box, (350, 410))
        pygame.display.flip()

    def check_valid_origin_selected(self, column, row):
        if self.board_state[column][row] != None:
            if self.board_state[column][row].colour == PLAYERS[self.player_turn]:
            # if we have selected our own colour peice
                return True
        return False

    def check_valid_input(self, temp_input):
        pattern = '[a-h][1-8][a-h][1-8]'
        if re.search(pattern, temp_input):
            origin_column = COLUMNS.index(temp_input[0])
            origin_row = ROWS.index(temp_input[1])
            if self.check_valid_origin_selected(origin_column, origin_row):
                origin_pos = (origin_column, origin_row)
                destination_column = COLUMNS.index(temp_input[2])
                destination_row = ROWS.index(temp_input[3])
                destination_pos = (destination_column, destination_row)
                if self.check_valid_move(origin_pos, destination_pos):
                    self.move_piece(origin_pos, destination_pos)
                return True
        return False

    def move_piece(self, origin_pos, destination_pos):
        origin_col, origin_row = origin_pos
        target_col, target_row = destination_pos
        moving_piece = self.board_state[origin_col][origin_row]
        moving_piece.move_to(destination_pos)
        if self.board_state[target_col][target_row] != None:
            self.board_state[target_col][target_row].kill()
        self.board_state[target_col][target_row] = moving_piece
        self.board_state[origin_col][origin_row] = None

    def test_pawn_rules(self, origin_pos, destination_pos):
        origin_col, origin_row = origin_pos
        target_col, target_row = destination_pos
        first_move = False
        # check if it's our pawn's first move
        if ((self.board_state[origin_col][origin_row].colour == 'Black' and origin_row == 1)
                or
                (self.board_state[origin_col][origin_row].colour == 'White' and origin_row == 6)
                ):
            first_move = True
        # check which direction we can move (up or down the board)
        if self.board_state[origin_col][origin_row].colour == 'Black':
            dir = 1
        else:
            dir = -1
        # pawns can move one step forward, if there is nothing there, 2 steps on their first move
        if (self.test_clear_path(origin_col, origin_row, target_col, target_row) and
                target_col == origin_col and
                (target_row - origin_row == dir or
                    (target_row - origin_row == dir * 2 and first_move))
                ):
            return True
        # if we're trying to take a piece
        elif self.board_state[target_col][target_row] != None:
            # and the piece we're trying to take is only 1 diagonal away
            # and the other colour to our current player
            if (abs(target_col - origin_col) == 1 and
                    abs(target_row - origin_row) == 1 and
                    self.board_state[target_col][target_row].colour != PLAYERS[self.player_turn]
                    ):
                return True
        return False

    def delta_norm(self, tar, ori):
        d = tar - ori
        if d != 0:
            d = int(d / abs(d))
        return int(d)

    def test_rook_rules(self, origin_pos, destination_pos):
        origin_col, origin_row = origin_pos
        target_col, target_row = destination_pos
        if (self.test_clear_path(origin_col, origin_row, target_col, target_row) and
                (target_col == origin_col or target_row == origin_row)
                ):
            return True
        elif self.board_state[target_col][target_row] != None:
            d_col = self.delta_norm(target_col, origin_col)
            d_row = self.delta_norm(target_row, origin_row)
        return False

    def test_clear_path(self, origin_col, origin_row, target_col, target_row):
        # need to normalise the delt column/row
        d_col = self.delta_norm(target_col, origin_col)
        d_row = self.delta_norm(target_row, origin_row)
        next_col = origin_col
        next_row = origin_row
        # see if we have a clear path to the destination
        while next_col != target_col or next_row != target_row:
            next_col += d_col
            next_row += d_row
            if self.board_state[next_col][next_row] != None:
                return False
        return True

    def check_valid_move(self, origin_pos, destination_pos):
        origin_col, origin_row = origin_pos
        piece_type = self.board_state[origin_col][origin_row].name
        if piece_type == 'Pawn':
            if self.test_pawn_rules(origin_pos, destination_pos):
                return True
        elif piece_type == 'Rook':
            if self.test_rook_rules(origin_pos, destination_pos):
                return True
        return False

    def text_input(self): # this creates a pop-up window to enter moves
        # clear last entry
        text = ''
        active = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # allow us to quit even if we're entering text
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(text) == 0:
                            # we haven't typed anything in, so close the text window
                            active = False
                        elif self.check_valid_input(text):
                            # the input is in a valid format
                            # and has selected a valid peice to move
                            active = False
                        else:
                            text = 'Not valid'
                    elif event.key == pygame.K_BACKSPACE:
                        # delete the last character
                        text = text[:-1]
                    elif len(text) < 4:
                        # add the typed character
                        text += event.unicode
                    # Re-render the text.
                    self.show_in_text_box(text)
            self.screen.blit(self.text_box, (350, 410))
            pygame.display.flip()

    def mouse_input(self, event_pos):
        column, row = self.xy_to_board(event_pos)
        if (column, row) == (99, 99):
            return
        if self.check_valid_origin_selected(column, row):
            origin_pos = (column, row)
            text = self.board_state[column][row].colour + ' ' + self.board_state[column][row].name 
            self.show_in_text_box(text)
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pass
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                            column, row = self.xy_to_board(event.pos)
                            destination_pos = (column, row)
                            if self.check_valid_move(origin_pos, destination_pos):
                                self.move_piece(origin_pos, destination_pos)
                                self.player_turn = 1 - self.player_turn
                            return
        else:
            text = 'invalid piece'
            self.show_in_text_box(text)
            time.sleep(1)

    def run(self):
        # we may want to load a different layout of pieces so we'll do that here
        all_pieces, self.board_state = self.add_pieces()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    raise SystemExit
                # if move == '' then no valid move was made
                elif event.type == pygame.TEXTINPUT:
                    self.text_input()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_input(event.pos)
            # Now you can just blit the background image
            self.screen.blit(self.background, (0, 0))
            #draw all the sprites to the screen
            all_pieces.draw(self.screen)

            pygame.display.flip()

# we decide to put the game logic on the Board
# the ChessPiece is just a visual representaiton with some local data
class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        pygame.sprite.Sprite.__init__(self, pieces_group)
        image_path = PATH + colour + '_' + piece_name + '.gif'
        self.name = piece_name
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx  = self.cr_to_xy(column)
        self.rect.centery = self.cr_to_xy(row)
        self.colour = colour
        self.selected = False
        self.first_move = True

    def cr_to_xy(self, num):
        # TILE_SIZE / 2 puts us in the middle of the tile
        # OFFSET accounts for the border
        # num * TILESIZE converts the column number to a x or y value
        return (TILE_SIZE / 2) + OFFSET + (num * TILE_SIZE)

    def move_to(self, destination_pos):
        target_col, target_row = destination_pos
        self.rect.centerx  = self.cr_to_xy(target_col)
        self.rect.centery = self.cr_to_xy(target_row)

def main():
    my_chess_game = Board()
    my_chess_game.run()

CWD = os.getcwd()
RESOURCES = '/Chess_Resources/'
PATH  = CWD + RESOURCES
pygame.init()

#set up board size
TILE_SIZE = 100
TILES = 8
OFFSET = 25
BOARD_SIZE = (TILE_SIZE * TILES) + (OFFSET * 2)
BLUE_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
BLUE_IMAGE.fill(pygame.Color('lightskyblue2'))
GRAY_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
GRAY_IMAGE.fill(pygame.Color('slategray4'))
FONT = pygame.font.Font(None, 32)

TEXT_COLOUR = pygame.Color('darkslategrey')
COLUMNS = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ROWS = [ '1', '2', '3', '4', '5', '6', '7', '8']

PLAYERS = ['White', 'Black']

if __name__ == '__main__':
    main()
import pygame, math, sys, itertools, re, os
import chess_pieces as cp
import chess_constants as cc
from pygame.math import Vector2

class Board():
    def __init__(self):
        # initalise pygame to start everything
        pygame.init()
        self.screen = pygame.display.set_mode((cc.BOARD_SIZE, cc.BOARD_SIZE))
        pygame.display.set_caption('Chess')
        self.background = self.make_background()
        self.text_box = self.add_text_box(110, 30)

    def add_text_box(self, w, h): # creates the basic text input box
        self.BOX_COLOUR = pygame.Color('coral')
        temp_text_box = pygame.Surface((w, h))
        temp_text_box.fill(self.BOX_COLOUR)
        return temp_text_box

    def check_valid_input(self, temp_input):
        pattern = '[a-h][1-8][a-h][1-8]'
        if re.search(pattern, temp_input) or len(temp_input) == 0:
            col_check = cc.COLUMNS.index(temp_input[0])
            row_check = cc.ROWS.index(temp_input[1])
            if self.board_state[col_check][row_check] != None:
                print(self.board_state[col_check][row_check])
                return True
        return False

    def text_input(self, x, y): # this creates a pop-up window to enter moves
        # clear last entry
        text = ''
        txt_surface = cc.FONT.render(text, True, cc.TEXT_COLOUR)
        self.text_box.fill(self.BOX_COLOUR)
        self.text_box.blit(txt_surface, (5, 5))
        active = True
        while active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # allow us to quit even if we're entering text
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        valid_input = self.check_valid_input(text)
                        if not valid_input:
                            txt_surface = cc.FONT.render('Not valid', True, cc.TEXT_COLOUR)
                            #clear box & re-blit
                            self.text_box.fill(self.BOX_COLOUR)
                            self.text_box.blit(txt_surface, (5, 5))
                            break
                        # end text entry and return to game
                        active = False
                    elif event.key == pygame.K_BACKSPACE:
                        # delete the last character
                        text = text[:-1]
                    elif len(text) < 4:
                        # add the typed character
                        text += event.unicode
                    # Re-render the text.
                    txt_surface = cc.FONT.render(text, True, cc.TEXT_COLOUR)
                    #clear box & re-blit
                    self.text_box.fill(self.BOX_COLOUR)
                    self.text_box.blit(txt_surface, (5, 5))
            self.screen.blit(self.text_box, (x, y))
            pygame.display.flip()
        return text

    def make_background(self): # this function creates a single image for the board squares and labels
        # set up a simple list of images that we can iterate through
        images = itertools.cycle((cc.BLUE_IMAGE, cc.GRAY_IMAGE))
        background = pygame.Surface((cc.BOARD_SIZE, cc.BOARD_SIZE))
        background.fill((255, 255, 255))
        # Use two nested for loops to get the coordinates.
        for row in range(cc.TILES):
            for column in range(cc.TILES):
                # This alternates between the blue and gray image.
                image = next(images)
                # Blit one image after the other at their respective coords
                background.blit(image, ((row * cc.TILE_SIZE) + cc.OFFSET, (column * cc.TILE_SIZE) + cc.OFFSET))
            next(images)
        background = self.mark_out(background)
        #returns a surface, ready to be sent to the screen
        return background

    def mark_out(self, background): # this function adds the column / row lables
        # position row labels
        for row, row_lable in enumerate(cc.ROWS):
            txt_image = cc.FONT.render(row_lable, True, (0, 0, 0))
            # labels up & down the left
            background.blit(txt_image, (5, (row * cc.TILE_SIZE) + (cc.OFFSET * 3)))
            # labels up and down the right, we use the same txt_image
            background.blit(txt_image, (cc.BOARD_SIZE - 20, (row * cc.TILE_SIZE) + (cc.OFFSET * 3)))
        for column, column_lable in enumerate(cc.COLUMNS):
            txt_image = cc.FONT.render(column_lable, True, (0, 0, 0))
            # labels along the top
            background.blit(txt_image, ((column * cc.TILE_SIZE) + (cc.OFFSET * 3), 5))
            # labels along the bottom, we use the same txt_image
            background.blit(txt_image, ((column * cc.TILE_SIZE) + (cc.OFFSET * 3), cc.BOARD_SIZE - 20))
        return background

    def load_pieces(self, file_name):
        input_file = open(cc.PATH + file_name, 'r')
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
        for column in range(0, cc.TILES):
                columnlist = []
                for row in range(0, cc.TILES):
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
            piece = cp.pieces[piece_index](piece_name, piece_colour, column, row, pieces_group)
            board_state[column][row] = piece
            pieces_group.add(piece)

        return pieces_group, board_state

    def piece_moved(event_pos, all_pieces, turn):
        for piece in all_pieces:
            #check to see if our mouseclick was on a piece and that it's our turn
            if piece.rect.collidepoint(event_pos) and piece.colour == turn:
                #we have clicked a piece - was it already selected
                if not piece.selected:
                    piece.selected = True
                    got_piece = True
                    return False
                else:
                    piece.selected = False
                    got_piece = False
            elif piece.selected:
                #move piece - need to check if move is valid
                if piece.valid_move(event_pos):
                    got_piece = False
                    return True
        return False

    def xy_to_board(self, pos):
        #first work out which row/column we clicked in
        column, row = pos
        column -= cc.OFFSET
        row -= cc.OFFSET
        aligned_column = math.trunc(column / cc.TILE_SIZE)
        aligned_row = math.trunc(row / cc.TILE_SIZE)
        aligned_square = [aligned_column, aligned_row]
        return aligned_square

    def mouse_input(self, event_pos):
        column, row = self.xy_to_board(event_pos)
        if self.board_state[column][row] != None:
            print(self.board_state[column][row])
        pass

    def run(self):
        # we may want to load a different layout of pieces so we'll do that here
        all_pieces, self.board_state = self.add_pieces()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                # if move == '' then no valid move was made
                elif event.type == pygame.TEXTINPUT:
                    move = self.text_input(375, 410)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    move = self.mouse_input(event.pos)

            # Now you can just blit the background image
            self.screen.blit(self.background, (0, 0))
            #draw all the sprites to the screen
            all_pieces.draw(self.screen)

            pygame.display.flip()

def main():
    my_chess_game = Board()
    my_chess_game.run()

if __name__ == '__main__':
    main()
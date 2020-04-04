'''
Chess, using pygame

- Chess is a two player game, no computer opponent yet
- We need a board graphic to position pieces on
- We need a set of white pieces and a set of black pieces
- Each piece has common func / att, and specific ones (the rules for how it can move)
- Moves are done by mouse-click
'''

import pygame, sys, itertools
import chess_constants as cc
import chess_pieces as cp
from pygame.math import Vector2
from pygame.locals import *

def draw_board(screen):
    images = itertools.cycle((cc.BLUE_IMAGE, cc.GRAY_IMAGE))
    background = pygame.Surface(screen.get_size())
    # Use two nested for loops to get the coordinates.
    for y in range(cc.TILES):
        for x in range(cc.TILES):
            # This alternates between the blue and gray image.
            image = next(images)
            # Blit one image after the other at their respective coords
            background.blit(image, (x*cc.TILE_SIZE, y*cc.TILE_SIZE))
        next(images)
    #returns a surface, ready to be sent to the screen
    return background

def add_pieces():
    #we place all our pieces in a group of sprites
    pieces_group = pygame.sprite.Group()
    for row in range(0,cc.TILES):
            rowlist = []
            for column in range(0,cc.TILES):
                if row == 0:
                    piece = cp.GameObject(cc.PATH +cc.IMAGES[column+8], 'black', column, row, pieces_group)
                elif row == 7:
                    piece = cp.GameObject(cc.PATH +cc.IMAGES[column], 'white', column, row, pieces_group)
                elif row == 6:
                    piece = cp.Pawn(cc.PATH +'White_Pawn.gif', 'white', column, row, pieces_group)
                elif row == 1:
                    piece = cp.Pawn(cc.PATH +'Black_Pawn.gif', 'black', column, row, pieces_group)
                else:
                    pass
                pieces_group.add(piece)
    return pieces_group

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

def main():
    #basic setup
    screen = pygame.display.set_mode((cc.BOARD_SIZE, cc.BOARD_SIZE))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    
    #create the background surface
    background = draw_board(screen)

    #set up a group for the pieces
    all_pieces = add_pieces()

    done = False
    got_piece = False
    turn = 'white'

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if piece_moved(event.pos, all_pieces, turn):
                    #we moved a piece, other player's turn
                    if turn == 'white':
                        turn = 'black'
                    else:
                        turn = 'white'
                pass

        # Now you can just blit the background image once
        screen.blit(background, (0, 0))
        #draw all the sprites to the screen
        all_pieces.draw(screen)

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
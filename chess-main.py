'''
Chess, using pygame

- Chess is a two player game, no computer opponent yet
- We need a board graphic to position pieces on
- We need a set of white pieces and a set of black pieces
- Each piece has common func / att, and specific ones (the rules for how it can move)
- Moves are done by mouse-click
'''

import pygame, sys, os, itertools
from pygame.math import Vector2
from pygame.locals import *

class GameObject():
    def __init__(self, icon, colour, x, y):
        self.icon = pygame.image.load(icon)
        self.icon_rect = self.icon.get_rect()
        self.icon_rect.top = x
        self.icon_rect.left = y
        self.colour = colour

    def draw_self(playing_area):
        playing_area.blit(self.icon, (self.icon_rect.top, self.icon_rect.left))
        return playing_area

class Pawn(GameObject):
    def __init__(self, icon, colour, x, y):
        super().__init__(icon, colour, x, y)

    def check_move(self, new_row_number,new_column_number):
        return True
#set up some constants
CWD = os.getcwd()
RESOURCES = '/Chess_Resources/'
PATH  = CWD + RESOURCES
ICONS = ['White_Rook.gif', 'White_Bishop.gif', 'White_Knight.gif', 'White_Queen.gif', 'White_King.gif', 'White_Knight.gif', 'White_Bishop.gif', 'White_Rook.gif', 'Black_Rook.gif', 'Black_Bishop.gif', 'Black_Knight.gif', 'Black_King.gif', 'Black_Queen.gif', 'Black_Knight.gif', 'Black_Bishop.gif', 'Black_Rook.gif'] #/media/barton_hill/THOMAS/ Digi@Local/MyCode/Python/4 - Green/Code/Chess_Resources/ gameOver = False
WHITE_PIECES = ['Rook', 'Bishop', 'Knight', 'Queen', 'King', 'Knight', 'Bishop', 'Rook']
BLACK_PIECES = ['Rook', 'Bishop', 'Knight', 'King', 'Queen', 'Knight', 'Bishop', 'Rook'] 

#set up board size
TILE_SIZE = 100
TILES = 8
BOARD_SIZE = TILE_SIZE * TILES
BLUE_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
BLUE_IMAGE.fill(pygame.Color('lightskyblue2'))
GRAY_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
GRAY_IMAGE.fill(pygame.Color('slategray4'))

def draw_board(screen):
    images = itertools.cycle((BLUE_IMAGE, GRAY_IMAGE))
    background = pygame.Surface(screen.get_size())
    # Use two nested for loops to get the coordinates.
    for y in range(TILES):
        for x in range(TILES):
            # This alternates between the blue and gray image.
            image = next(images)
            # Blit one image after the other at their respective coords.
            background.blit(image, (x*TILE_SIZE, y*TILE_SIZE))
        next(images)
    return background

def add_pieces():
    pieces_group = pygame.sprite.Group()
    for row in range(0,TILES):
            rowlist = []
            for column in range(0,TILES):
                if row == 0:
                    pieces_group.add(GameObject(PATH +ICONS[column+8], 'black', column + 10, row + 10))
                elif row == 7:
                    pieces_group.add(GameObject(PATH +ICONS[column], 'white', column + 10, row + 10))
                elif row == 6:
                    pieces_group.add(Pawn('Pawn', PATH +'White_Pawn.gif', 'white', column + 10, row + 10))
                elif row == 1:
                    pieces_group.add(Pawn('Pawn', PATH +'Black_Pawn.gif', 'black', column + 10, row + 10))
                else:
                    pass
    return pieces_group


def main():
    #basic setup
    screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
    pygame.display.set_caption('Chess')
    clock = pygame.time.Clock()
    
    #create the background surface
    background = draw_board(screen)

    #set up a group for the pieces - not quite working yet, WIP
    #all_pieces = add_pieces()

    done = False

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Now you can just blit the background image once
        # instead of blitting thousands of separate images.
        screen.blit(background, (0, 0))

        pygame.display.flip()
        clock.tick(60)

if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
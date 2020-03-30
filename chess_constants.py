import pygame, os
#set up some constants
CWD = os.getcwd()
RESOURCES = '/Chess_Resources/'
PATH  = CWD + RESOURCES
IMAGES = ['White_Rook.gif', 'White_Bishop.gif', 'White_Knight.gif', 'White_Queen.gif', 'White_King.gif', 'White_Knight.gif', 'White_Bishop.gif', 'White_Rook.gif', 'Black_Rook.gif', 'Black_Bishop.gif', 'Black_Knight.gif', 'Black_King.gif', 'Black_Queen.gif', 'Black_Knight.gif', 'Black_Bishop.gif', 'Black_Rook.gif'] #/media/barton_hill/THOMAS/ Digi@Local/MyCode/Python/4 - Green/Code/Chess_Resources/ gameOver = False
WHITE_PIECES = ['Rook', 'Bishop', 'Knight', 'Queen', 'King', 'Knight', 'Bishop', 'Rook']
BLACK_PIECES = ['Rook', 'Bishop', 'Knight', 'King', 'Queen', 'Knight', 'Bishop', 'Rook'] 

#set up board size
TILE_SIZE = 100
TILES = 8
OFFSET = 15
BOARD_SIZE = TILE_SIZE * TILES
BLUE_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
BLUE_IMAGE.fill(pygame.Color('lightskyblue2'))
GRAY_IMAGE = pygame.Surface((TILE_SIZE,TILE_SIZE))
GRAY_IMAGE.fill(pygame.Color('slategray4'))
import pygame, os
pygame.init()
#set up some constants
CWD = os.getcwd()
RESOURCES = '/Chess_Resources/'
PATH  = CWD + RESOURCES

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
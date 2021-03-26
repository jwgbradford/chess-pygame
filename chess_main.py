import pygame

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
import pygame, itertools

class Board():
    def __init__(self):
        self.screen = pygame.display.set_mode((BOARD_SIZE, BOARD_SIZE))
        pygame.display.set_caption('Chess')
        self.background = self.make_background()

    def make_background(self):
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
        return background

    def run(self):
        while True:
            self.screen.blit(self.background, (0, 0))
            pygame.display.flip()

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

if __name__ == '__main__':
    my_chess_game = Board()
    my_chess_game.run()
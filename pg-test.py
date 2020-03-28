import itertools

import pygame
from pygame.math import Vector2

LENGTH = 100
BLUE_IMAGE = pygame.Surface((LENGTH, LENGTH))
BLUE_IMAGE.fill(pygame.Color('lightskyblue2'))
GRAY_IMAGE = pygame.Surface((LENGTH, LENGTH))
GRAY_IMAGE.fill(pygame.Color('slategray4'))

def draw_board(screen):
    images = itertools.cycle((BLUE_IMAGE, GRAY_IMAGE))
    background = pygame.Surface(screen.get_size())
    # Use two nested for loops to get the coordinates.
    for y in range(screen.get_height()//LENGTH):
        for x in range(screen.get_width()//LENGTH):
            # This alternates between the blue and gray image.
            image = next(images)
            # Blit one image after the other at their respective coords.
            background.blit(image, (x*LENGTH, y*LENGTH))
        next(images)
    return background

def main():
    screen = pygame.display.set_mode((800, 800))
    clock = pygame.time.Clock()
    all_pieces = pygame.sprite.Group()

    background = draw_board(screen)
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
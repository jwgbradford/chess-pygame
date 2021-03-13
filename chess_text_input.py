import pygame
from pygame.locals import *

TEXT_COLOUR = pygame.Color('coral')
BOX_COLOUR = pygame.Color('darkslategrey')
FONT = pygame.font.Font(None, 32)

class InputBox:
    def __init__(self, x, y, w, h):
        self.text_box = pygame.Surface((w, h))
        self.x, self.y = x, y
        self.text_box.fill(BOX_COLOUR)
        self.text_colour = TEXT_COLOUR
        self.text = ''
        self.txt_surface = FONT.render(text, True, self.text_colour)
        self.active = False

    def text_input(self, screen):
        self.active = True
        while self.active:
            for event in pygame.event.get():
                if event.type == QUIT:
                    # allow us to quit even if we're entering text
                    pygame.quit()
                    raise SystemExit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # end text entry and return to game
                        self.active = False
                    elif event.key == pygame.K_BACKSPACE:
                        # delete the last character
                        self.text = self.text[:-1]
                    else:
                        # add the typed character
                        self.text += event.unicode
                    # Re-render the text.
                    self.txt_surface = FONT.render(self.text, True, self.text_colour)
            screen.blit(self.txt_surface, (self.text_box.x+5, self.text_box.y+5))
            pygame.display.update()
        return self.text
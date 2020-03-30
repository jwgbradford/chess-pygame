import pygame

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, colour, x, y, pieces_group):
        pygame.sprite.Sprite.__init__(self, pieces_group) 
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.top = x
        self.rect.left = y
        self.colour = colour
        self.selected = False

class Pawn(GameObject):
    def __init__(self, image, colour, x, y, pieces_group):
        super().__init__(image, colour, x, y, pieces_group)

    def check_move(self, new_row_number,new_column_number):
        return True
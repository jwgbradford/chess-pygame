import pygame, math
import chess_constants as cc

class GameObject(pygame.sprite.Sprite):
    def __init__(self, image, colour, column, row, pieces_group):
        pygame.sprite.Sprite.__init__(self, pieces_group) 
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.top = cr_to_board(column)
        self.rect.left = cr_to_board(row)
        self.colour = colour
        self.selected = False

    def valid_move(self, event_pos):
        self.move_piece(event_pos)
        return True

    def move_piece(self, event_pos):
        self.rect.top = xy_to_board(event_pos[1])
        self.rect.left = xy_to_board(event_pos[0])
        self.selected = False

class Pawn(GameObject):
    def __init__(self, image, colour, column, row, pieces_group):
        super().__init__(image, colour, column, row, pieces_group)
        self.first_move = True

    def valid_move(self, event_pos):
        self.move_piece(event_pos)
        return True

def cr_to_board(num):
    return (num * cc.TILE_SIZE) + cc.OFFSET

def xy_to_board(pos):
    #first work out which row/column we clicked in
    aligned_int = math.trunc(pos / cc.TILE_SIZE)
    #then convert back to x/y coordinates for pygame
    aligned_pos = (aligned_int * cc.TILE_SIZE) + cc.OFFSET
    return aligned_pos
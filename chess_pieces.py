import pygame, math
import chess_constants as cc

class GameObject(pygame.sprite.Sprite):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        pygame.sprite.Sprite.__init__(self, pieces_group)
        image_path = cc.PATH + colour + '_' + piece_name + '.gif'
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.left = self.cr_to_board(column)
        self.rect.top = self.cr_to_board(row)
        self.colour = colour
        self.selected = False

    def valid_move(self, event_pos): #holding code - returns true if no local rules defined for piece
        self.move_piece(event_pos)
        return True

    def move_piece(self, event_pos):
        self.rect.top = xy_to_board(event_pos[1])
        self.rect.left = xy_to_board(event_pos[0])
        self.selected = False

    def cr_to_board(self, num):
        return (num * cc.TILE_SIZE) + cc.OFFSET * 1.5

class Pawn(GameObject):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        super().__init__(piece_name, colour, column, row, pieces_group)
        self.first_move = True

    def valid_move(self, event_pos):
        current_y_column = self.cr_to_board(self.rect.left)
        ypos = event_pos[1]
        y_column = xy_to_board(ypos)
        print(current_y_column, y_column)
        if self.colour == 'white' and y_column == current_y_column + 1:
            self.move_piece(event_pos)
            return True
        return False

class Rook(GameObject):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        super().__init__(piece_name, colour, column, row, pieces_group)

class Knight(GameObject):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        super().__init__(piece_name, colour, column, row, pieces_group)

class Bishop(GameObject):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        super().__init__(piece_name, colour, column, row, pieces_group)

class Queen(GameObject):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        super().__init__(piece_name, colour, column, row, pieces_group)

class King(GameObject):
    def __init__(self, piece_name, colour, column, row, pieces_group):
        super().__init__(piece_name, colour, column, row, pieces_group)

pieces = [Pawn, Rook, Knight, Bishop, Queen, King]
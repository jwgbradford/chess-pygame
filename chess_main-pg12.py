import pygame, itertools, os

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
        background = self.mark_out(background)
        return background

    def mark_out(self, background):
        for row, row_lable in enumerate(ROWS):
            txt_image = FONT.render(row_lable, True, TEXT_COLOUR)
            # labels up & down the left
            background.blit(txt_image, (5, (row * TILE_SIZE) + (OFFSET * 3)))
            # labels up and down the right, we use the same txt_image
            background.blit(txt_image, (BOARD_SIZE - 20, (row * TILE_SIZE) + (OFFSET * 3)))
        for column, column_lable in enumerate(COLUMNS):
            txt_image = FONT.render(column_lable, True, TEXT_COLOUR)
            # labels along the top
            background.blit(txt_image, ((column * TILE_SIZE) + (OFFSET * 3), 5))
            # labels along the bottom, we use the same txt_image
            background.blit(txt_image, ((column * TILE_SIZE) + (OFFSET * 3), BOARD_SIZE - 20))
        return background

    def load_pieces(self, file_name):
        input_file = open(PATH + file_name, 'r')
        input_data = input_file.readlines()
        input_file.closed
        input_split = []
        for entry in input_data:
            split_data = entry.split(', ')
            input_split.append(split_data)
        return input_split

    def add_pieces(self):
        pieces_list = self.load_pieces('test_board_layout.txt')
        pieces_group = pygame.sprite.Group()
        board_state = []
        for column in range(0, TILES):
                columnlist = []
                for row in range(0, TILES):
                    columnlist.append(None)
                board_state.append(columnlist)
        for entry in pieces_list:
            piece_colour = entry[0]
            piece_name = entry[1]
            column = int(entry[2])
            row = int(entry[3])
            piece = ChessPiece(piece_name, piece_colour, column, row)
            board_state[column][row] = piece
            pieces_group.add(piece)
        return pieces_group, board_state

    def run(self):
        all_pieces, self.board_state = self.add_pieces()
        while True:
            self.screen.blit(self.background, (0, 0))
            all_pieces.draw(self.screen)
            pygame.display.flip()

class ChessPiece(pygame.sprite.Sprite):
    def __init__(self, piece_name, colour, column, row):
        pygame.sprite.Sprite.__init__(self)
        image_path = PATH + colour + '_' + piece_name + '.gif'
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.rect.centerx  = self.cr_to_xy(column)
        self.rect.centery = self.cr_to_xy(row)
        self.name = piece_name
        self.colour = colour

    def cr_to_xy(self, num):
        return (TILE_SIZE / 2) + OFFSET + (num * TILE_SIZE)

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
FONT = pygame.font.Font(None, 32)
TEXT_COLOUR = pygame.Color('darkslategrey')
COLUMNS = [ 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
ROWS = [ '1', '2', '3', '4', '5', '6', '7', '8']
CWD = os.getcwd()
RESOURCES = '/Chess_Resources/'
PATH  = CWD + RESOURCES

if __name__ == '__main__':
    my_chess_game = Board()
    my_chess_game.run()
'''
Chess, using pygame

- Chess is a two player game, no computer opponent yet
- This is our main programme, most of the action is in chess_board and chess_pieces
  but we use this in case we want to add a welcome screen, loading functions, etc
- We need a board graphic to position pieces on
- We need a set of white pieces and a set of black pieces
- Each piece has common func / attributes, and specific ones (the rules for how it can move)
- Moves are done by mouse-click
'''

import chess_board as cb

def main():
    my_chess_game = cb.Board()
    my_chess_game.main()

if __name__ == '__main__':
    main()
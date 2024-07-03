from game.chess_engine.app.board import *
from game.chess_engine.app.moves import *

def create_new_board():
    #starts a new board
    board = Board()
    return board.board


def move(pos_i,_pos_f):
    """
    If movement is impossible then returns None
    If possible then returns new board 
    """
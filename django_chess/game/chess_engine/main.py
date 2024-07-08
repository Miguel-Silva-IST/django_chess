from game.chess_engine.app.board import *
from game.chess_engine.app.moves import *

def create_new_board():
    #starts a new board
    board = Board()
    return board.board


def move(board_state,pos_i,pos_f):
    board = Board(board_state)
    piece_number = board_state[pos_i[0]][pos_i[1]]
    piece = board.get_board_piece(pos_i)
    check_moves = PossibleMoves(board, piece)
    check_moves.check_possible_moves()
    if pos_f in check_moves.possible_moves:
        board_state[pos_f[0]][pos_f[1]] = board_state[pos_i[0]][pos_i[1]]
        board_state[pos_i[0]][pos_i[1]] = None
        return board_state
    else:
        return False

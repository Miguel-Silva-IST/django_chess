"""Module with multiple distinct classes and functions that are used across the code"""

from .colors import BLACK, WHITE
from .board import *
import copy



def check_board_in_boundaries(board,pos):
    """
    Retusn 1 if in boundaries, 0 if out
    """
    
    if 0<=pos[0]<len(board.board) and 0<=pos[1]<len(board.board):
        return 1
    else:
        return 0



def find_king(piece, board):
    """Returns king value"""
    
    if piece.color == WHITE:
        king_val = BoardMapping('WKI').val
    elif piece.color == BLACK:
        king_val == BoardMapping('BKI').val
    
    
    board_size = len(board)
    
    for r in range(board_size):
        for c in range(board_size):
            if board_size[r][c] == king_val:
                king_pos = [r,c]
                break
    
    return board.get_board_piece(king_pos)
            


def verify_piece_in_line_king(piece, king):
    """
    Function used to avoid verify unecessary checks. Returns 1 if in line
    """
    
    #verify rows, cols, diag
    if piece.pos[0] == king.pos[0]:
        return 1
    elif piece.pos[1] == king.pos[1]:
        return 1
    elif abs(piece.pos[0] - king.pos[0])/abs(piece.pos[1]-king.pos[1]) == 1:
        return 1
    else:
        return 0 
    
    
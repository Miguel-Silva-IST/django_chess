def add_index_chessboard(chessboard):
    i = 0
    indexed_chessboard = []
    for row in chessboard:
        aux_row = []
        for square in row:
            aux_row.append([square,i])
            i+=1
        indexed_chessboard.append(aux_row)
    return indexed_chessboard


def remove_index_chessboard(indexed_chessboard):
    return [[sublist[0] for sublist in row] for row in indexed_chessboard]




def convert_index_to_pos(index, board):
    board_w = len(board[0])
    r = index//board_w
    c = index - r*board_w
    return [r,c]


def convert_pos_to_index(pos, board):
    board_w = len(board[0])
    index = pos[0]*board_w + pos[1]
    return index
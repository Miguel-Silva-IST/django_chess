def index_chessboard(chessboard):
    i = 0
    indexed_chessboard = []
    for row in chessboard:
        aux_row = []
        for square in row:
            aux_row.append([square,i])
            i+=1
        indexed_chessboard.append(aux_row)
    return indexed_chessboard
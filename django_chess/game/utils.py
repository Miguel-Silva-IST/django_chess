from player.models import Player
from game.models import Game
import json
from django.db.models import Q

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



def get_player_from_request(request = False, body = False):
    """If suk_player = False then it gets player from user object
       Else gets player from suk_player in body
    """
    if body:
        suk_player = body['suk_player']
        player = Player.objects.filter(suk_player=suk_player).first()
    else:
        user = request.user
        player = Player.objects.filter(user=user).first()
    return player



def get_active_game(player):
    '''
    Gets last active game for player object
    '''
    suk_player = player.suk_player
    last_active_game = Game.objects.filter(Q(suk_player_1 = suk_player) | Q(suk_player_2 = suk_player), game_active = True ).first()
    return last_active_game

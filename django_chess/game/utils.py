from player.models import Player
from game.models import Game
import json
from django.db.models import Q
from .models import Game, GameDetail
from django.core.cache import cache

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
        cached_player_object = cache.get(suk_player)
        #if cached, returns cached value
        if cached_player_object:
            return cached_player_object
        else:
            #caches object to avoid query for every call
            player_object = Player.objects.filter(suk_player=suk_player).first()
            cache.set(suk_player,player_object)
            return player_object

    else:
        user = request.user
        cached_player_object = cache.get(user)
        #if cached, returns cached value
        if cached_player_object:
            return cached_player_object
        else:
            #caches object to avoid query for every call
            player_object = Player.objects.filter(user=user).first()
            cache.set(user,player_object)
            return player_object



def get_active_game(player):
    '''
    Gets last active game for player object
    '''
    suk_player = player.suk_player
    cached_active_game = cache.get(f'active_game_{suk_player}')
    #if cached, returns cached value
    if cached_active_game:
        return cached_active_game
    else:
        #caches object to avoid query for every call
        last_active_game = Game.objects.filter(Q(suk_player_1 = suk_player) | Q(suk_player_2 = suk_player), game_active = True ).first()
        cache.set(f'active_game_{suk_player}', last_active_game)
        return last_active_game



def get_last_board_state(last_active_game):
    cached_board_state = cache.get(last_active_game)
    if cached_board_state:
        print('cached_board_state')
        return cached_board_state
    else:
        board_state = GameDetail.objects.filter(suk_game = last_active_game.suk_game).order_by('-id').first().board_state
        cache.set(last_active_game, board_state)
        return board_state
    


#def clean_cache(active_game_cache = False, board_state_cache = False):
#    if active_game_cache:
#        cache.delete(active_game_cache)
#    if board_state_cache:
#        cache.delete(board_state_cache)

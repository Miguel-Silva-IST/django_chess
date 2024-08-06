from game.chess_engine.app.board import *
from game.chess_engine.app.moves import *
from game.chess_engine.app.player import *
from django.core.cache import cache

def create_new_board():
    #starts a new board
    board = Board()
    return board.board



def check_move(board_state,pos_i,pos_f, last_active_game):
    #player = Player(WHITE)
    board = Board(board_state)
    piece = board.get_board_piece(pos_i)
    #if no piece in the initial position then false
    if not piece:
       return False
    
    #verify if player played in his/her turn
    player_turn_to_play = cache.get(f'player_to_play_{last_active_game.suk_game}')
    if player_turn_to_play == None:
        player_turn_to_play = WHITE
    
    if not piece.color ==  player_turn_to_play:
        print(f'Is {player_turn_to_play} turn to play')
        return False

    player = Player(piece.color) #only using object to store player color...
    piece_move_object = piece.move(board,piece)
    piece_move_object.check_possible_moves()
    possible_moves = piece_move_object.possible_moves
    if pos_f in possible_moves:
        board_state[pos_f[0]][pos_f[1]] = board_state[pos_i[0]][pos_i[1]]
        board_state[pos_i[0]][pos_i[1]] = None

        #check if new board state has king being checked: if y then impossible move, else possible
        new_board_object = Board(board_state)
        verify_check = VerifyCheck(new_board_object, player)
        result = verify_check.verify_check()
        if result:
            print(f'King {player.color} is checked')
            return False
        else:
            next_player_to_play = switch_player_turn_to_play(player_turn_to_play)
            cache.set(f'player_to_play_{last_active_game.suk_game}', next_player_to_play)
            return board_state


        return board_state
    else:
        return False

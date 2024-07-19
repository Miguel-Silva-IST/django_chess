from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse,JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from game.chess_engine.main import *
from .utils import add_index_chessboard, convert_index_to_pos
from .models import Game, GameDetail
from player.models import Player
import json



def home(request):
    return render(request, 'game/index.html')



def about(request):
    return render(request, 'game/about.html')



def play(request):
    return render(request, 'game/play.html')


@login_required
def sandbox(request):
    """
    First checks for any active game user might have to avoid lost games
    If user still has active game, then it loads the last board state and game
    is resumed. Else it starts a new game and renders the new game board. 
    """
    if request.method == 'GET':
        #find if there are active games for user
        user = request.user
        player = Player.objects.filter(user=user).first()
        last_active_game = Game.objects.filter(Q(suk_player_1 = player.suk_player) | Q(suk_player_2 = player.suk_player), game_active = True ).first()
        #if no active games then starts one
        if not last_active_game:
            #creates new game
            game = Game(suk_player_1 = player,suk_player_2 = player, game_active = True)
            game.save()
            #inserts first row in game detail
            board_state = create_new_board()
            game_detail = GameDetail(suk_game = game, suk_player = player, board_state = board_state)
            game_detail.save()

        #if game still ative, returns from the last game
        else:
            board_state = GameDetail.objects.filter(suk_game = last_active_game.suk_game).order_by('-id').first().board_state
            
        
        indexed_chessboard = add_index_chessboard(board_state)[::-1]
        dic_pieces = {
            -1 : '<i class="fa-regular fa-chess-pawn"></i>',
            -2 : '<i class="fa-regular fa-chess-rook"></i>',
            -3 : '<i class="fa-regular fa-chess-knight"></i>',
            -4 : '<i class="fa-regular fa-chess-bishop"></i>',
            -5 : '<i class="fa-regular fa-chess-queen"></i>',
            -6 : '<i class="fa-regular fa-chess-king"></i>',
             1 : '<i class="fa-solid fa-chess-pawn"></i>',
             2 : '<i class="fa-solid fa-chess-rook"></i>',
             3 : '<i class="fa-solid fa-chess-knight"></i>',
             4 : '<i class="fa-solid fa-chess-bishop"></i>',
             5 : '<i class="fa-solid fa-chess-queen"></i>',
             6 : '<i class="fa-solid fa-chess-king"></i>',
             None : ''
        }
        return render(request, 'game/sandbox.html', context = {'chessboard':board_state,'indexed_chessboard':indexed_chessboard, 'dic_pieces':dic_pieces, 'suk_player': player.suk_player})


def move(request):
    """
    Receives POST request with new move. Evaluates if the move is possible and returns 
    the new updated board if move is possible. Else it returns data = {'move':False}
    """
    if request.method == 'POST':
        #parses request body
        decoded_body = request.body.decode('utf-8')
        body = json.loads(decoded_body)
        suk_player = body['suk_player']
        indexed_moves = body['moves']
        #gets last board state
        player = Player.objects.filter(suk_player=suk_player).first()
        last_active_game = Game.objects.filter(Q(suk_player_1 = suk_player) | Q(suk_player_2 = suk_player), game_active = True ).first()
        #if user has no active game
        if not last_active_game:
            print('No games active for user')
            data = {'move':False}
            return JsonResponse(data)
        
        board = GameDetail.objects.filter(suk_game = last_active_game.suk_game).latest('id').board_state
        #checks move possibility
        moves = [convert_index_to_pos(index, board) for index in indexed_moves]
        move_result =  check_move(board,moves[0],moves[1])
        #if there is a new move, then updates database and sends the new board state back to template
        if move_result:
            data = {'move':True, 'updated_board':move_result}
            game_detail = GameDetail(suk_game = last_active_game, suk_player = player, board_state = move_result)
            game_detail.save()
        else:
            data = {'move':False}
        
        return JsonResponse(data)        
        

def end_game(request):
    """Updates the active game field to False"""
    if request.method == 'POST':

        decoded_body = request.body.decode('utf-8')
        body = json.loads(decoded_body)
        suk_player = body['suk_player']
        #updates active game active=False
        last_active_game = Game.objects.filter(Q(suk_player_1 = suk_player) | Q(suk_player_2 = suk_player), game_active = True ).first()
        if not last_active_game:
            print('Game already finished')
            return JsonResponse({'end_game':'sucess'})    
        last_active_game.game_active = False
        last_active_game.save()
        return JsonResponse({'end_game':'sucess'})



@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "game" / "static" / "game" / "favicon.png").open("rb")
    return FileResponse(file)





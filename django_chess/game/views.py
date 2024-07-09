from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse,JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from game.chess_engine.main import *
from urllib.parse import unquote_plus
from .utils import add_index_chessboard, remove_index_chessboard, convert_index_to_pos
import json, ast



def home(request):
    return render(request, 'game/index.html')



def about(request):
    return render(request, 'game/about.html')



def play(request):
    return render(request, 'game/play.html')


def sandbox(request):
    #when tsrating adds count+1 to games
    #starts a new detail game as well and keeps on adding moves
    #initiates a board and passes it as context
    if request.method == 'GET':
        #take into account if page is refreshed, game is lost
        chessboard = create_new_board()
        indexed_chessboard = add_index_chessboard(chessboard)
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
        return render(request, 'game/sandbox.html', context = {'chessboard':chessboard,'indexed_chessboard':indexed_chessboard, 'dic_pieces':dic_pieces})





@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "game" / "static" / "game" / "favicon.png").open("rb")
    return FileResponse(file)




def move(request):
    if request.method == 'POST':
        decoded_body = request.body.decode('utf-8')
        body = json.loads(decoded_body)
        board = body['board']
        #added because the first time the board is acessed is through context var. Need to replace by postgres database. Howver makes more sense to replace None by 0 since js cant parse None...
        if isinstance(board, str):
            try:
                board = eval(body['board'])
            except:
                raise Exception(f'Couldnt parse board {body}')
        
        moves = [convert_index_to_pos(index, board) for index in body['moves']]
        move_result =  check_move(board,moves[0],moves[1])
        if move_result:
            data = {'move':True, 'updated_board':move_result}
        else:
            data = {'move':False}
        
        print(data)
        
        return JsonResponse(data)






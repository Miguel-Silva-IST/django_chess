from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse,JsonResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from game.chess_engine.main import *
import json
from urllib.parse import unquote_plus
from .utils import index_chessboard




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
        indexed_chessboard =index_chessboard(chessboard)
        print('SANDBOX VIEW')
        print(indexed_chessboard)
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
        return render(request, 'game/sandbox.html', context = {'indexed_chessboard':indexed_chessboard, 'dic_pieces':dic_pieces})





@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "game" / "static" / "game" / "favicon.png").open("rb")
    return FileResponse(file)




def test(request):
    if request.method == 'POST':
        body = request.body.decode('utf-8')
        board_str = json.loads(body)['board']
        try:
            board = eval(board_str) #doesnt seem good solution...
        except:
            raise Exception('Failed to parse board')
        
        indexed_chessboard =index_chessboard(board)
        
        data = {'board':indexed_chessboard}
        return JsonResponse(data)
    else:
        data = {'message': 'Hello, World!'}
        return JsonResponse(data)






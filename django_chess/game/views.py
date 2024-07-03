from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET
from game.chess_engine.main import *




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
        board = create_new_board()
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
        return render(request, 'game/sandbox.html', context = {'board':board, 'dic_pieces':dic_pieces})





@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "game" / "static" / "game" / "favicon.png").open("rb")
    return FileResponse(file)






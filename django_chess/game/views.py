from django.shortcuts import render
from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET




def home(request):
    
    context = {'test' : 1}
    return render(request, 'game/index.html', context)



def about(request):
    return render(request, 'game/about.html')



def play(request):
    return render(request, 'game/play.html')


@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "game" / "static" / "game" / "favicon.png").open("rb")
    return FileResponse(file)




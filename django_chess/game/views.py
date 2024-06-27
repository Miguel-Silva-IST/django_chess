from django.shortcuts import render



def home(request):
    
    context = {'test' : 1}
    return render(request, 'game/index.html', context)



def about(request):
    return render(request, 'game/about.html')



def play(request):
    return render(request, 'game/play.html')




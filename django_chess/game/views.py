from django.shortcuts import render



def home(request):
    
    context = {'test' : 1}
    return render(request, 'game/index.html', context)

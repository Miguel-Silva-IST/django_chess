from django.shortcuts import render



def home(request):
    
    context = {'test' : 1}
    return render(request, 'django_chess/index.html', context)

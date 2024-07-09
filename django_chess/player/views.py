from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Player
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from player.forms import PlayerForm


#signup page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #Uppon signup it also creates new Player object
            last_created_player = Player.objects.order_by('-suk_player').first()
            if not last_created_player:
                #first user being created
                suk_new_player = 1
            else:
                #else, increments last player suk by 1
                suk_new_player = last_created_player.suk_player + 1
            new_player = Player(user = new_user,suk_player = suk_new_player, username = new_user.username)
            new_player.save()
            messages.success(request, 'Your acount has been created')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'player/signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    player = Player.objects.filter(user=request.user).first()

    if request.method == 'GET':
        return render(request,'player/profile.html', context={'player':player})
    elif request.method=='POST':
        form = PlayerForm(request.POST, request.FILES, instance=player)
        if form.is_valid():
            form.save()
            return render(request,'player/profile.html', context = {'player':player})
        else:
            form = PlayerForm()
            return render(request,'player/profile.html', context={'form':PlayerForm(instance=player)})
    
    return render(request,'player/profile.html', context={'player':player})


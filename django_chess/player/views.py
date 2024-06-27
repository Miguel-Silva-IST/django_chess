from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from .models import Player

#signup page
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            #Uppon signup it also creates new Player object
            last_created_player = Player.objects.order_by('suk_player').first()
            if not last_created_player:
                #first user being created
                suk_new_player = 1
            else:
                #
                suk_new_player = last_created_player.suk_player + 1
            new_player = Player(user = new_user,suk_player = suk_new_player, nm_player = new_user.username, email_player = 'No email added')
            new_player.save()
            messages.success(request, 'Your acount has been created')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'player/signup.html', {'form': form})

def profile(request):
    return render(request,'player/profile.html')

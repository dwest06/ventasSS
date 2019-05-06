""" Vistas para el control de usuarios """

from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .forms import LoginForm

# Create your views here.

def login_user(request):

    if request.user.is_authenticated:
        return redirect('ventas:index')
    
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        next = request.GET.get('next')
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next) if next else redirect('/')
    else:
        form = LoginForm()

    return render(request, 'registration/login.html', {'form' : form})
            
@login_required
def logout_user(request):

    if request.method == "POST":
        logout(request)
    
    return redirect('usuarios:login')
from django.shortcuts import render
from .models import Pessoa
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect


def registrar_user_view(resquest):
    if resquest.method == 'POST':

        username = resquest.POST.get("username")
        email = resquest.POST.get("email")
        password = resquest.POST.get("password")

        criando_user = User.objects.create_user(
            username=username,
            email=email,
            password=password)

        return redirect('login')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)
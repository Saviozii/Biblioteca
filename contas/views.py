from django.shortcuts import render
from .models import Pessoa
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages

def registrar_user_view(request):
    if request.method == 'POST':

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        nome = request.POST.get("nome")
        turma_id = request.POST.get("turma")

        criando_user = User.objects.create_user(
            username=username,
            email=email,
            password=password
            )

        Pessoa.objects.create(
            usuario=criando_user,
            nome=nome,
            turma_id=turma_id
        )

        return redirect('login')

    return render(request, 'cadastro.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

    user = authenticate(request, email=email, password=password)

    if user is not None:
        login(request, user)

        #RAMON LEMBRA DE DEPOIS ADCIONAR O REDDIRECT PRO ADMIN
        return redirect ('')

    else:
        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request , 'login.html')


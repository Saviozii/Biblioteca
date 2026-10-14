from django.shortcuts import render
from .models import Pessoa
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from function_view import todos_livros, recomendações
from django.contrib.auth.decorators import login_required, user_passes_test

#Verifica se é adm
def is_staff(usuario):
    return usuario.is_staff

def base_catalogo(request):
    elements = {
        "All_livros":todos_livros(),
        "Recomendation": recomendações(),

    }
    return render(request,"catalogo.html",{'elements':elements})


@user_passes_test(is_staff, login_url='login')
def base_admin(request):
    ...
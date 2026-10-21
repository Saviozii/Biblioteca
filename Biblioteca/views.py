from django.shortcuts import render
from .models import Pessoa
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from function_view import todos_livros, recomendações, pedir_livro
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from .function_view import pedir_livro

#Verifica se é adm
def is_staff(usuario):
    return usuario.is_staff

def base_catalogo(request):
    elements = {
        "All_livros":todos_livros(),
        "Recomendation": recomendações()
    }
    return render(request,"catalogo.html",{'elements':elements})

@login_required
def inf_livro(request,livro_id):
    livro = get_object_or_404(livro, id=livro_id)
    back_url = request.META.get('HTTP_REFERER', '/Catalogo')
    elements = {
    "Livro":livro,
    "Back_url":back_url,
    "Pedir_Livro":pedir_livro(request,livro_id)
    }
    return render(request,"inf_livro.html",{"elements":elements})
         
@user_passes_test(is_staff, login_url='login')
def base_admin(request):
    ...
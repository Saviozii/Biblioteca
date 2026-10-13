from django.shortcuts import render
from .models import Pessoa
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from function_view import livros


def base_catalogo(request):
    elements = {
        "All_livros":livros,
    }
    return render(request,"catalogo.html",{'elements':elements})
from django.shortcuts import render
from .models import Pessoa, Livro, Emprestimo
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .function_view import todos_livros, recomendações, pedir_livro, adcionar_livro
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404
from django.contrib import messages
from datetime import date, timedelta

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
    livro = get_object_or_404(Livro,id=livro_id)
    pessoa = getattr(request.user, "pessoa", None)
    prazo = date.today() + timedelta(days=15)

    #Função pedir livro
    if request.method == "POST":
        if pessoa is None:
                messages.error(request,"Usuario não possui cadastro.")
        else:
             if livro.esta_emprestado:
                  messages.error(request,f"O livro '{livro.titulo}' já está emprestado.")
             else:
                  pedir_livro(pessoa,livro,prazo)
                  messages.success(request,f"Boa Leitura!!!😁, O livro deve ser entregue até dia {prazo:%d/%m/%Y}")
                  return redirect("Catalogo")
  
    return render(request, "inf_livro.html", {"livro": livro})


@user_passes_test(is_staff, login_url='login')
def base_admin(request):
    return render(request,"base_admin.html")

@user_passes_test(is_staff, login_url='login')
def adcionar_livro_view(request):
     add_livro = adcionar_livro(request)
     return render(request,"add_livro.html",{'add_livro':add_livro})
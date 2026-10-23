from .forms import Form_Livro
from .models import Livro, Turmas, Emprestimo
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from datetime import date, timedelta
#Consultas:

def todas_turmas():
    turma = Turmas.objects.all()
    return turma

def todos_livros():
    livros = Livro.objects.all()
    return livros

def recomendações():
    mais_emprestados = Livro.objects.annotate(
        total_emprestimos=Count('emprestimos')
    ).order_by('-total_emprestimos')[:10]
    return mais_emprestados



#pagina usuario:
def pedir_livro(pessoa,livro,prazo):
    Emprestimo.objects.create(
        pessoa=pessoa,
        livro=livro,
        data_devolucao_prevista=prazo,
    )

#Para pagina adm:

def adcionar_livro(request):
    if request.method == 'POST':
        adcionando_livro = Form_Livro(request.POST, request.FILES)

        if adcionando_livro.is_valid():
            livro = adcionando_livro.save()
            messages.success(
                request,
                f'O livro "{livro.titulo}" foi adicionado ao acervo.',
            )
            return Form_Livro()
    else:
        adcionando_livro = Form_Livro()

    return adcionando_livro


def livros_emprestados():
    emprestados = Emprestimo.objects.filter(status="E")
    total_emprestados = Emprestimo.objects.filter(status="E").count()
    return emprestados, total_emprestados


def efetuar_devolução(request,emprestimo_id):
    
    if request.method != "POST":
        return redirect ('admin_base')
    
    emprestimo = get_object_or_404(
        Emprestimo,
        id=emprestimo_id
    )

    if emprestimo.status == "E":
        emprestimo.status = "D"
        emprestimo.save()
        messages.success(request,f"O Livro {emprestimo.livro.titulo} foi devolvido com sucesso!.")
        return redirect ('admin_base')

from .forms import Form_Livro
from .models import Livro, Turmas, Emprestimo
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction
from .models import Livro, Emprestimo
from datetime import date, timedelta
#Consultas:

def todas_turmas(Turmas):
    turma = Turmas.objects.all()
    return turma


def todos_livros(Livro):
    livros = Livro.objects.all()
    return livros

def recomendações(Livro):
    mais_emprestados = Livro.objects.annotate(
        tota_emprestimos=Count('emprestimo')
    ).order_by('-total_emprestimos')[:10]
    return mais_emprestados

def livros_emprestados():
    emprestados = Emprestimo.objects.filter(status="E")
    total_emprestados = Emprestimo.objects.filter(status="E").count()
    return emprestados, total_emprestados


#Para pagina publica
@login_required
def pedir_livro(request,livro_id):
    if request.method != "POST":
        return redirect("Catalogo")

    pessoa = getattr(request.user, "pessoa", None)
    if pessoa is None:
        messages.error(request, "Seu usuário não tem cadastro")
        return redirect("Catalogo")

    livro = get_object_or_404(Livro, id=livro_id)
    tem_livro = Emprestimo.objects.filter(livro=livro, status="E").exists()
    prazo = date.today() + timedelta(days=15)

    if tem_livro:
        messages.error(request,f"O livro {livro} já está emprestado")
        return redirect("Catalogo")
    else:
        Emprestimo.objects.create(
            pessoa=pessoa,
            livro=livro,
            data_devolucao_prevista=prazo,
        )

    messages.success(
        request,
        f"O livro “{livro.titulo}” foi emprestado.E deve ser entregue até {prazo:%d/%m/%Y}.",
    )
    return redirect("catalogo")
        


#Para pagina adm:

def adcionar_livro(request):

    if request.method == 'POST':
        adcionando_livro = Form_Livro(request.POST,request.FILES)

        if adcionando_livro.is_valid():
            adcionando_livro.save()

        print(f"O livro {Livro.titulo} foi adcionardo por {request.user}")

    else: adcionando_livro = Form_Livro()

def efetuar_devolução(request):
    ...
 

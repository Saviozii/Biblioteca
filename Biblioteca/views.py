from django.shortcuts import render
from .models import Pessoa, Livro, Emprestimo, Turmas
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .function_view import (todos_livros, recomendações, 
                            pedir_livro, adcionar_livro, 
                            todas_turmas, alunos_da_Turma,
                            livros_emprestados, histoico_livro)
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



#ADMIN
@user_passes_test(is_staff, login_url='login')
def base_admin(request):
     
     return render(request,"base_admin.html")

@user_passes_test(is_staff, login_url='login')
def analise_consulta(request):
    emprestados, total_emprestados = livros_emprestados()
    elements = {
        "Todas_Turmas": todas_turmas(),
        "LivrosEmprestados": emprestados,
        "TotalEmprestados": total_emprestados,
    }

    #Colsultas
    turma_id = request.GET.get("turma_id", "")
    if turma_id.isdigit():
        turma = get_object_or_404(Turmas, id=turma_id)
        elements["turma_selecionada"] = turma
        elements["Alunos_da_Turma_Selecionada"] = alunos_da_Turma(turma.id)
    elif turma_id:
        messages.error(request, "Turma inválida.")

    usuario_id = request.GET.get("usuario_id", "")
    if usuario_id.isdigit():
        elements["Usuario_selecionado"] = get_object_or_404(Pessoa, id=usuario_id)
    elif usuario_id:
        messages.error(request, "Usuário inválido.")

    return render(request, "analise.html", elements)


@user_passes_test(is_staff, login_url='login')
def adcionar_livro_view(request):
     add_livro = adcionar_livro(request)
     return render(request,"add_livro.html",{'add_livro':add_livro})

@user_passes_test(is_staff, login_url='login')
def Usuario_inf(request,usuario_id):
     usuario = get_object_or_404(Pessoa,id=usuario_id)
     historico = list(histoico_livro(usuario))
     hoje = date.today()

     ativos = [emp for emp in historico if emp.status == "E"]
     devolvidos = [emp for emp in historico if emp.status == "D"]

     for emp in historico:
          emp.atrasado = False
          emp.dias_restantes = None
          emp.dias_atraso = 0
          if emp.status == "E" and emp.data_devolucao_prevista:
               emp.dias_restantes = (emp.data_devolucao_prevista - hoje).days
               if emp.dias_restantes < 0:
                    emp.atrasado = True
                    emp.dias_atraso = abs(emp.dias_restantes)

     atrasados = [emp for emp in ativos if emp.atrasado]
     proximo_vencimento = min(
          (emp.data_devolucao_prevista for emp in ativos if emp.data_devolucao_prevista),
          default=None,
     )

     return render(request,"inf_usuario.html",{
          "usuario":usuario,
          "Historico":historico,
          "Resumo":{
               "total": len(historico),
               "ativos": len(ativos),
               "devolvidos": len(devolvidos),
               "atrasados": len(atrasados),
          },
          "Proximo_vencimento":proximo_vencimento,
          })
from .forms import Form_Livro
from .models import Livro, Turmas

def adcionar_livro(request):

    if request.method == 'POST':
        adcionando_livro = Form_Livro(request.POST,request.FILES)

        if adcionando_livro.is_valid():
            adcionando_livro.save()

        print(f"O livro {Livro.titulo} foi adcionardo por {request.user}")

    else: adcionando_livro = Form_Livro()


def todas_turmas(Turmas):
    turma = Turmas.objects.all()
    return turma


livros = Livro.objects.all()



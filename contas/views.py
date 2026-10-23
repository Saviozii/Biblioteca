from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import CadastroForm


def registrar_user_view(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso. Faça login.')
            return redirect('login')
    else:
        form = CadastroForm()

    return render(request, 'cadastro.html', {'form': form})


def login_view(request):
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print(f"O usuario {user} logou")

            next_url = request.POST.get('next') or request.GET.get('next')
            if next_url and url_has_allowed_host_and_scheme(
                next_url,
                allowed_hosts={request.get_host()},
            ):
                return redirect(next_url)

            if user.is_staff:
                return redirect('admin_base')

            return redirect('Catalogo')

        messages.error(request, 'Usuário ou senha inválidos.')

    return render(request, 'login.html')


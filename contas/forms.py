from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction

from Biblioteca.models import Pessoa, Turmas


class CadastroForm(UserCreationForm):
    nome = forms.CharField(max_length=100)
    email = forms.EmailField()
    turma = forms.ModelChoiceField(queryset=Turmas.objects.all())

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username",)

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]

        if commit:
            user.save()
            Pessoa.objects.create(
                usuario=user,
                nome=self.cleaned_data["nome"],
                turma=self.cleaned_data["turma"],
            )

        return user

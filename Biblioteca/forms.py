from django import forms
from .models import Livro


class Form_Livro(forms.ModelForm):
    class Meta:
        model = Livro
        fields = [
            'titulo',
            'autor',
            'genero',
            'capa',
            'descricao'
        ]
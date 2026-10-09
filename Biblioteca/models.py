from django.db import models
from django.contrib.auth.models import User

class Turmas(models.Model):
    turma = models.CharField(max_length=100)

    def __str__(self):
        return self.turma

class Pessoa(models.Model):
    
    usuario = models.OneToOneField(User,on_delete=models.CASCADE,related_name="pessoa")
    turma = models.ForeignKey(Turmas,on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
 
    def __str__(self):
        return self.usuario.username


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    genero = models.CharField(max_length=100)
    capa = models.ImageField(upload_to="capas/", blank=True, null=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.titulo


class Biblioteca(models.Model):
    data = models.DateField(db_index=True)
    data_do_emprestimo = models.DateField(null=True, blank=True)
    data_da_devolucao = models.DateField(null=True, blank=True)
    usuario = models.ForeignKey(Pessoa,on_delete=models.CASCADE)
    livros = models.ForeignKey(Livro,on_delete=models.CASCADE)
    
    STATUS = (
        ("A","Armazenado"),
        ("E", "Emprestado"),
        ("D", "Devolvido"),)
    status = models.CharField(max_length=1,choices=STATUS, default="A")

class Emprestimo(models.Model):
    user = models.ForeignKey(Pessoa,on_delete=models.CASCADE)
    




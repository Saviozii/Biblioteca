from django.db import models
from django.db.models import Q
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
        return self.nome


class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    autor = models.CharField(max_length=150)
    genero = models.CharField(max_length=100)
    capa = models.ImageField(upload_to="capas/", blank=True, null=True)
    descricao = models.TextField(blank=True)

    def __str__(self):
        return self.titulo

    @property
    def esta_emprestado(self):
        return self.emprestimos.filter(status="E").exists()

    @property
    def disponivel(self):
        return not self.esta_emprestado
    

class Emprestimo(models.Model):
    pessoa = models.ForeignKey(Pessoa,on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro,on_delete=models.CASCADE)
    data_emprestimo = models.DateField(auto_now_add=True)
    data_devolucao_prevista = models.DateField(null=True, blank=True)
    data_devolvido = models.DateTimeField(null=True, blank=True)
    STATUS = (
        ("E","Emprestado"),
        ("D","Devolvido"),
    )
    status= models.CharField(max_length=1,choices=STATUS,default="E")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["livro"],
                condition=Q(status="E"),
                name="um_emprestimo_ativo_por_livro",
            )
        ]





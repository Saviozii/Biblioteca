import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Biblioteca', '0002_pessoa_nome_emprestimo'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emprestimo',
            name='user',
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='pessoa',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='emprestimos',
                to='Biblioteca.pessoa',
            ),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='livro',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='emprestimos',
                to='Biblioteca.livro',
            ),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='data_emprestimo',
            field=models.DateField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='data_devolucao_prevista',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='data_devolvido',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='emprestimo',
            name='status',
            field=models.CharField(
                choices=[('E', 'Emprestado'), ('D', 'Devolvido')],
                default='E',
                max_length=1,
            ),
        ),
        migrations.AddConstraint(
            model_name='emprestimo',
            constraint=models.UniqueConstraint(
                condition=models.Q(('status', 'E')),
                fields=('livro',),
                name='um_emprestimo_ativo_por_livro',
            ),
        ),
        migrations.DeleteModel(
            name='biblioteca',
        ),
    ]

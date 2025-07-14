from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('Pages', '0011_grupomuscular_remove_exercicio_categoria_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='treinoaluno',
            name='template_origem',
        ),
        migrations.DeleteModel(
            name='TreinoPredefExercicio',
        ),
        migrations.DeleteModel(
            name='TreinoPredefinido',
        ),
        migrations.AddField(
            model_name='treinoaluno',
            name='exercicios',
            field=models.ManyToManyField(blank=True, related_name='treinos', through='Pages.TreinoAlunoExercicio', to='Pages.exercicio'),
        ),
    ]

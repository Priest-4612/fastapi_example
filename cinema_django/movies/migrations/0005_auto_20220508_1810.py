# Generated by Django 3.2 on 2022-05-08 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0004_auto_20220505_0139'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='filmworkgenre',
            name='unique_film_work_genre',
        ),
        migrations.RemoveConstraint(
            model_name='filmworkperson',
            name='unique_film_work_person_role_idx',
        ),
        migrations.RemoveIndex(
            model_name='filmworkperson',
            name='film_work_person_idx',
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='type',
            field=models.TextField(choices=[('movie', 'Movie'), ('tv_show', 'Tv Show')], default='movie', verbose_name='type'),
        ),
        migrations.AlterField(
            model_name='filmworkperson',
            name='role',
            field=models.TextField(choices=[('actor', 'Actor'), ('director', 'Director'), ('producer', 'Producer'), ('writer', 'Writer')], default='actor', verbose_name='role'),
        ),
        migrations.AddIndex(
            model_name='filmworkperson',
            index=models.Index(fields=['film_work', 'person'], name='film_work_person_idx'),
        ),
        migrations.AddConstraint(
            model_name='filmworkgenre',
            constraint=models.UniqueConstraint(fields=('film_work', 'genre'), name='unique_film_work_genre'),
        ),
        migrations.AddConstraint(
            model_name='filmworkperson',
            constraint=models.UniqueConstraint(fields=('film_work', 'person', 'role'), name='unique_film_work_person_role_idx'),
        ),
    ]

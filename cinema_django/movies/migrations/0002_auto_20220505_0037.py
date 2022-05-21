# Generated by Django 3.2 on 2022-05-04 21:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(related_name='filmworks', through='movies.FilmworkGenre', to='movies.Genre', verbose_name='genres'),
        ),
        migrations.AlterField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(related_name='filmworks', through='movies.FilmworkPerson', to='movies.Person', verbose_name='persons'),
        ),
        migrations.AlterField(
            model_name='filmworkgenre',
            name='film_work',
            field=models.ForeignKey(db_column='film_work_id', on_delete=django.db.models.deletion.CASCADE, related_name='genre_film_work', to='movies.filmwork', verbose_name='film_work'),
        ),
        migrations.AlterField(
            model_name='filmworkgenre',
            name='genre',
            field=models.ForeignKey(db_column='genre_id', on_delete=django.db.models.deletion.CASCADE, related_name='genre_film_work', to='movies.genre', verbose_name='genre'),
        ),
        migrations.AlterField(
            model_name='filmworkperson',
            name='film_work',
            field=models.ForeignKey(db_column='film_work_id', on_delete=django.db.models.deletion.CASCADE, related_name='person_film_work', to='movies.filmwork', verbose_name='film_work'),
        ),
        migrations.AlterField(
            model_name='filmworkperson',
            name='person',
            field=models.ForeignKey(db_column='person_id', on_delete=django.db.models.deletion.CASCADE, related_name='person_film_work', to='movies.person', verbose_name='person'),
        ),
    ]

# Generated by Django 3.0.5 on 2020-11-20 20:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_auto_20201120_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='api.Title', verbose_name='Фильм'),
        ),
        migrations.AlterField(
            model_name='title',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category_titles', to='api.Category', verbose_name='Категория фильма'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(blank=True, related_name='genre_titles', to='api.Genre', verbose_name='Жанр фильма'),
        ),
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Фильм'),
        ),
    ]

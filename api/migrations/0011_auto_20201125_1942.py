# Generated by Django 3.0.5 on 2020-11-25 19:42

import api.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20201122_1334'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveSmallIntegerField(blank=True, db_index=True, validators=[api.validators.year_validator], verbose_name='Год выхода'),
        ),
    ]

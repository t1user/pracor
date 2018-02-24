# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-24 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0075_auto_20180213_1859'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interview',
            name='how_got',
            field=models.CharField(choices=[('A', 'Ogłoszenie'), ('B', 'Kontakty zawodowe'), ('C', 'Head-hunter'), ('D', 'Znajomi/rodzina'), ('F', 'Targi/prezentacje'), ('G', 'Strona internetowa firmy'), ('H', 'Inne')], default=None, max_length=1, verbose_name='droga do interview'),
        ),
    ]
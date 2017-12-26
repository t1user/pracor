# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-23 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0056_auto_20171202_1905'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interview',
            options={'verbose_name': 'Rozmowa', 'verbose_name_plural': 'Rozmowy'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Opinia', 'verbose_name_plural': 'Opinie'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='advancement',
        ),
        migrations.RemoveField(
            model_name='company',
            name='compensation',
        ),
        migrations.RemoveField(
            model_name='company',
            name='environment',
        ),
        migrations.RemoveField(
            model_name='company',
            name='number_of_reviews',
        ),
        migrations.RemoveField(
            model_name='company',
            name='overallscore',
        ),
        migrations.RemoveField(
            model_name='company',
            name='worklife',
        ),
        migrations.AlterField(
            model_name='interview',
            name='how_got',
            field=models.CharField(choices=[('A', 'Ogłoszenie'), ('B', 'Kontakty profesjonalne'), ('C', 'Head-hunter'), ('D', 'Znajomi/rodzina'), ('E', 'Seks z decydentem'), ('F', 'Targi/prezentacje'), ('F', 'Inne')], default=None, max_length=1, verbose_name='droga do interview'),
        ),
        migrations.AlterField(
            model_name='position',
            name='company_linkedin_id',
            field=models.CharField(blank=True, default='', max_length=25),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='position',
            name='company_name',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
    ]
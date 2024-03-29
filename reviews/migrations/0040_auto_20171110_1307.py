# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-10 12:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0039_auto_20171023_1852'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='salary',
            name='base_annual',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Pensja zasadnicza rocznie'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='base_monthly',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Pensja zasadnicza miesięcznie'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus_gross_net',
            field=models.CharField(choices=[('G', 'brutto'), ('N', 'netto')], default='G', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus_input',
            field=models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='premia'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus_period',
            field=models.CharField(choices=[('M', 'miesięcznie'), ('K', 'kwartalnie'), ('R', 'rocznie'), ('G', 'na godzinę')], default='R', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='gross_net',
            field=models.CharField(choices=[('G', 'brutto'), ('N', 'netto')], default='G', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='period',
            field=models.CharField(choices=[('M', 'miesięcznie'), ('K', 'kwartalnie'), ('R', 'rocznie'), ('G', 'na godzinę')], default='M', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='total_annual',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Pensja całkowita rocznie'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='total_monthly',
            field=models.PositiveIntegerField(default=0, editable=False, verbose_name='Pensja całkowita miesięcznie'),
        ),
    ]

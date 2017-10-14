# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-14 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0032_auto_20171014_2324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Zatwierdzone'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Zatwierdzone'),
        ),
        migrations.AlterField(
            model_name='review',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Zatwierdzone'),
        ),
        migrations.AlterField(
            model_name='review',
            name='comment',
            field=models.TextField(blank=True, max_length=500, verbose_name='co należy zmienić'),
        ),
        migrations.AlterField(
            model_name='review',
            name='cons',
            field=models.TextField(max_length=500, verbose_name='wady'),
        ),
        migrations.AlterField(
            model_name='review',
            name='pros',
            field=models.TextField(max_length=500, verbose_name='zalety'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='approved',
            field=models.BooleanField(default=False, verbose_name='Zatwierdzone'),
        ),
    ]
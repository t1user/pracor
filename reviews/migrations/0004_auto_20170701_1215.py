# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-01 10:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_remove_company_number_of_reviews'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='advancement',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='możliwości rozwoju'),
        ),
        migrations.AlterField(
            model_name='review',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Company'),
        ),
        migrations.AlterField(
            model_name='review',
            name='compensation',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='zarobki'),
        ),
        migrations.AlterField(
            model_name='review',
            name='environment',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='atmosfera w pracy'),
        ),
        migrations.AlterField(
            model_name='review',
            name='overallscore',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='ocena ogólna'),
        ),
        migrations.AlterField(
            model_name='review',
            name='worklife',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='równowaga praca-życie'),
        ),
    ]
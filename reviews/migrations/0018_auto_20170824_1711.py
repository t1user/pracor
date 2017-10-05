# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-24 15:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0017_auto_20170824_1706'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='career_start_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('M', 'Mężczyzna'), ('K', 'Kobieta')], max_length=1, null=True),
        ),
    ]
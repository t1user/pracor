# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-09 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'verbose_name': 'Profil', 'verbose_name_plural': 'Profile'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='contributed',
            field=models.BooleanField(default=False),
        ),
    ]
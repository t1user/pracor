# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-13 22:49
from __future__ import unicode_literals

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20171009_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='contributed',
            field=models.BooleanField(default=False, verbose_name='Zrobił wpis'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='sex',
            field=models.CharField(blank=True, choices=[('K', 'Kobieta'), ('M', 'Mężczyzna')], default=None, max_length=1, null=True, verbose_name='płeć'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]

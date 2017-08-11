# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 12:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_auto_20170707_1249'),
    ]

    operations = [
        migrations.RenameField(
            model_name='salary',
            old_name='gross_net_bonus',
            new_name='bonus_gross_net',
        ),
        migrations.RenameField(
            model_name='salary',
            old_name='bonus',
            new_name='bonus_input',
        ),
        migrations.RenameField(
            model_name='salary',
            old_name='time_unit',
            new_name='period',
        ),
        migrations.RemoveField(
            model_name='salary',
            name='time_unit_bonus',
        ),
        migrations.AddField(
            model_name='salary',
            name='bonus_period',
            field=models.CharField(choices=[('M', 'miesięcznie'), ('R', 'rocznie'), ('G', 'na godzinę')], default='M', max_length=1),
        ),
    ]
# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-03 13:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0023_auto_20170912_1225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='position',
            name='location',
            field=models.CharField(max_length=50, null=True),
        ),
    ]

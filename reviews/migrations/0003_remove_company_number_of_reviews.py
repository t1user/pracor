# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-30 20:09
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20170613_2005'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='number_of_reviews',
        ),
    ]
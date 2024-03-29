# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-24 14:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0015_auto_20170824_1515'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='linkedin_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='linkedin_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]

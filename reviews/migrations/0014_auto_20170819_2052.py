# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-19 18:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0013_positions'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positions',
            name='company_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='positions',
            name='linkedin_id',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='positions',
            name='start_date_month',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='positions',
            name='start_date_year',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]

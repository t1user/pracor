# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-07 18:41
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0010_auto_20170707_1429'),
    ]

    operations = [
        migrations.CreateModel(
            name='Interview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now=True)),
                ('position', models.CharField(blank=True, max_length=100, verbose_name='stanowisko')),
                ('department', models.CharField(blank=True, max_length=100, verbose_name='departament')),
                ('how_got', models.CharField(choices=[('A', 'Ogłoszenie'), ('B', 'Kontakty profesjonalne'), ('C', 'Head-hunter'), ('D', 'Znajomi-rodzina'), ('E', 'Sex z decydentem'), ('F', 'Inne')], default=None, max_length=1, verbose_name='droga do interview')),
                ('difficulty', models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], verbose_name='trudność')),
                ('got_offer', models.BooleanField(verbose_name='czy dostał ofertę')),
                ('questions', models.TextField(verbose_name='pytania')),
                ('impressions', models.CharField(blank=True, max_length=100, verbose_name='wrażenia')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.Company')),
            ],
        ),
        migrations.AddField(
            model_name='review',
            name='title',
            field=models.CharField(default='Ciekawa recenzja.', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus_gross_net',
            field=models.CharField(choices=[('G', 'brutto'), ('N', 'netto')], default='G', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus_input',
            field=models.PositiveIntegerField(default=0, verbose_name='premia'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='bonus_period',
            field=models.CharField(choices=[('M', 'miesięcznie'), ('R', 'rocznie'), ('G', 'na godzinę')], default='M', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='currency',
            field=models.CharField(default='PLN', max_length=3, verbose_name='waluta'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='gross_net',
            field=models.CharField(choices=[('G', 'brutto'), ('N', 'netto')], default='G', max_length=1, verbose_name=''),
        ),
        migrations.AlterField(
            model_name='salary',
            name='period',
            field=models.CharField(choices=[('M', 'miesięcznie'), ('R', 'rocznie'), ('G', 'na godzinę')], default='M', max_length=1, verbose_name='za okres'),
        ),
        migrations.AlterField(
            model_name='salary',
            name='salary_input',
            field=models.PositiveIntegerField(verbose_name='pensja'),
        ),
    ]

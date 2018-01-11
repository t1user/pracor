# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-01-02 19:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0054_auto_20171201_2124'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='interview',
            options={'verbose_name': 'Rozmowa', 'verbose_name_plural': 'Rozmowy'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Opinia', 'verbose_name_plural': 'Opinie'},
        ),
        migrations.RemoveField(
            model_name='company',
            name='advancement',
        ),
        migrations.RemoveField(
            model_name='company',
            name='compensation',
        ),
        migrations.RemoveField(
            model_name='company',
            name='environment',
        ),
        migrations.RemoveField(
            model_name='company',
            name='number_of_reviews',
        ),
        migrations.RemoveField(
            model_name='company',
            name='overallscore',
        ),
        migrations.RemoveField(
            model_name='company',
            name='worklife',
        ),
        migrations.AlterField(
            model_name='company',
            name='ownership',
            field=models.TextField(blank=True, null=True, verbose_name='właściciele'),
        ),
        migrations.AlterField(
            model_name='company',
            name='sectors',
            field=models.TextField(blank=True, null=True, verbose_name='sektory'),
        ),
        migrations.AlterField(
            model_name='interview',
            name='how_got',
            field=models.CharField(choices=[('A', 'Ogłoszenie'), ('B', 'Kontakty profesjonalne'), ('C', 'Head-hunter'), ('D', 'Znajomi/rodzina'), ('E', 'Seks z decydentem'), ('F', 'Targi/prezentacje'), ('F', 'Inne')], default=None, max_length=1, verbose_name='droga do interview'),
        ),
        migrations.AlterField(
            model_name='position',
            name='company_linkedin_id',
            field=models.CharField(blank=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='position',
            name='start_date_year',
            field=models.PositiveIntegerField(choices=[(2018, 2018), (2017, 2017), (2016, 2016), (2015, 2015), (2014, 2014), (2013, 2013), (2012, 2012), (2011, 2011), (2010, 2010), (2009, 2009), (2008, 2008), (2007, 2007), (2006, 2006), (2005, 2005), (2004, 2004), (2003, 2003), (2002, 2002), (2001, 2001), (2000, 2000), (1999, 1999), (1998, 1998), (1997, 1997), (1996, 1996), (1995, 1995), (1994, 1994), (1993, 1993), (1992, 1992), (1991, 1991), (1990, 1990), (1989, 1989), (1988, 1988), (1987, 1987), (1986, 1986), (1985, 1985), (1984, 1984), (1983, 1983), (1982, 1982), (1981, 1981), (1980, 1980), (1979, 1979), (1978, 1978), (1977, 1977), (1976, 1976), (1975, 1975), (1974, 1974), (1973, 1973), (1972, 1972), (1971, 1971)], default=None, null=True),
        ),
    ]
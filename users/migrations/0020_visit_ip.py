# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-02-12 17:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_profile_email_confirmed'),
    ]

    operations = [
        migrations.AddField(
            model_name='visit',
            name='ip',
            field=models.GenericIPAddressField(blank=True, editable=False, null=True, unpack_ipv4=True),
        ),
    ]

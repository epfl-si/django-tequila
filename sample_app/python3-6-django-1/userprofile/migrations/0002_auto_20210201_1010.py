# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2021-02-01 10:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='sciper',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
    ]
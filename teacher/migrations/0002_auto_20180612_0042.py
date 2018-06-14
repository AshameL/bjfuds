# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-12 00:42
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='errorque',
            name='testid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Questionitem'),
        ),
        migrations.AlterField(
            model_name='referencefile',
            name='chapter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='student.Chapter'),
        ),
    ]

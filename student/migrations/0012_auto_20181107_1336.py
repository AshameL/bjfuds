# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-11-07 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0011_auto_20181107_1336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='subchapter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Subchapter'),
        ),
        migrations.AlterField(
            model_name='questionitem',
            name='subchapterid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Subchapter'),
        ),
        migrations.AlterField(
            model_name='subchapter',
            name='chapterid',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='student.Chapter'),
        ),
    ]

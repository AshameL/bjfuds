# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-12 02:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0010_auto_20180612_0205'),
        ('teacher', '0002_auto_20180612_0042'),
    ]

    operations = [
        migrations.CreateModel(
            name='QueAccurancy',
            fields=[
                ('id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='student.Questionitem')),
                ('correctCount', models.IntegerField(default=0)),
                ('wrongCount', models.IntegerField(default=0)),
            ],
        ),
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

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Politician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=5)),
                ('photo', models.URLField()),
                ('pid', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SubmitLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=50)),
                ('shown_list', models.CharField(max_length=100)),
                ('select_list', models.CharField(max_length=70)),
                ('q_kind', models.CharField(max_length=5)),
            ],
        ),
    ]

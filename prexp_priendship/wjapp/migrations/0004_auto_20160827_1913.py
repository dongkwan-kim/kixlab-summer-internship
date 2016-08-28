# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wjapp', '0003_votevector'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoBillNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p1', models.CharField(max_length=5)),
                ('p2', models.CharField(max_length=5)),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='VoteNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('p1', models.CharField(max_length=5)),
                ('p2', models.CharField(max_length=5)),
                ('weight', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='lwjnetwork',
            name='do_i_have',
        ),
    ]

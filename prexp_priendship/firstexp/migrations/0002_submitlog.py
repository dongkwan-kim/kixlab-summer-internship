# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstexp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubmitLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=50)),
                ('shown_list', models.CharField(max_length=30)),
                ('select_list', models.CharField(max_length=30)),
            ],
        ),
    ]

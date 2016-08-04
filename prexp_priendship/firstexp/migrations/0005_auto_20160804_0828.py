# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstexp', '0004_submitlog_q_kind'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submitlog',
            name='select_list',
            field=models.CharField(max_length=70),
        ),
        migrations.AlterField(
            model_name='submitlog',
            name='shown_list',
            field=models.CharField(max_length=100),
        ),
    ]

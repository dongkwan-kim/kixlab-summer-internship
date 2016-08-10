# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('secondexp', '0002_remove_submitlog_q_kind'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submitlog',
            name='select_list',
        ),
        migrations.AddField(
            model_name='submitlog',
            name='affinity_score',
            field=models.CharField(default='1', max_length=15),
            preserve_default=False,
        ),
    ]

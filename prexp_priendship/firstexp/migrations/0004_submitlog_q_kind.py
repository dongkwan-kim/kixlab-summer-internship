# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstexp', '0003_politician_pid'),
    ]

    operations = [
        migrations.AddField(
            model_name='submitlog',
            name='q_kind',
            field=models.CharField(default='a', max_length=5),
            preserve_default=False,
        ),
    ]

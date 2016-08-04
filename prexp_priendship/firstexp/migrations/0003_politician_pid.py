# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('firstexp', '0002_submitlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='politician',
            name='pid',
            field=models.IntegerField(default=-1),
            preserve_default=False,
        ),
    ]

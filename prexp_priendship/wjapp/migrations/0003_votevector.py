# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wjapp', '0002_vote19'),
    ]

    operations = [
        migrations.CreateModel(
            name='VoteVector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=5)),
                ('party', models.CharField(max_length=10)),
                ('vote', models.TextField()),
            ],
        ),
    ]

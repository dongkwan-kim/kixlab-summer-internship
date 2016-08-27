# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wjapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vote19',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=5)),
                ('party', models.CharField(max_length=10)),
                ('vote', models.TextField()),
            ],
        ),
    ]

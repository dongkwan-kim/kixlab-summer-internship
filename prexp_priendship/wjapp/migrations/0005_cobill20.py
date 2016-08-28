# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wjapp', '0004_auto_20160827_1913'),
    ]

    operations = [
        migrations.CreateModel(
            name='CoBill20',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('bill_no', models.IntegerField()),
                ('p_list', models.TextField()),
            ],
        ),
    ]

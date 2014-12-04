# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='downtime',
            name='starts',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 4, 12, 19, 34, 260043), auto_now=True),
            preserve_default=False,
        ),
    ]

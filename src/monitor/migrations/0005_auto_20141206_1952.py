# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0004_auto_20141206_1911'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='downtime',
            name='checks',
        ),
        migrations.RemoveField(
            model_name='downtime',
            name='monitor',
        ),
        migrations.DeleteModel(
            name='DownTime',
        ),
    ]

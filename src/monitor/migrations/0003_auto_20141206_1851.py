# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0002_downtime_starts'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='check',
            options={'ordering': ('-capture',)},
        ),
        migrations.RemoveField(
            model_name='monitor',
            name='current_state',
        ),
    ]

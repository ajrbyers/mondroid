# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0005_auto_20141206_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check',
            name='capture',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]

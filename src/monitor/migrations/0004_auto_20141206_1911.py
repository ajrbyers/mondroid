# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0003_auto_20141206_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monitor',
            name='url',
            field=models.URLField(help_text=b'The URL to be monitored.', unique=True, max_length=2000),
            preserve_default=True,
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('monitor', '0006_auto_20141207_1724'),
    ]

    operations = [
        migrations.AddField(
            model_name='monitor',
            name='slug',
            field=models.SlugField(default='test1', help_text=b'Slug of the name, or another slug of your choosing.', max_length=200),
            preserve_default=False,
        ),
    ]

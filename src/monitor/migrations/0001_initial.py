# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Check',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status_code', models.CharField(max_length=10)),
                ('history', models.CharField(max_length=2000)),
                ('elapsed_time', models.CharField(max_length=200)),
                ('up', models.BooleanField(default=True)),
                ('capture', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DownTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('active', models.BooleanField(default=True)),
                ('checks', models.ManyToManyField(to='monitor.Check')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Monitor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b"A Monitor's display name.", max_length=200)),
                ('url', models.URLField(help_text=b'The URL to be monitored.', max_length=2000)),
                ('current_state', models.ForeignKey(related_name='current_state', blank=True, to='monitor.Check', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='downtime',
            name='monitor',
            field=models.ForeignKey(to='monitor.Monitor'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='check',
            name='monitor',
            field=models.ForeignKey(to='monitor.Monitor'),
            preserve_default=True,
        ),
    ]

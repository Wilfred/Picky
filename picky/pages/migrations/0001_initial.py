# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200, unique=True, null=True)),
                ('name_slug', models.CharField(max_length=200, unique=True, null=True, editable=False)),
                ('name_lower', models.CharField(max_length=200, null=True, editable=False)),
                ('content', models.TextField(blank=True)),
                ('deleted', models.BooleanField(default=False)),
                ('total_revisions', models.IntegerField(default=0, editable=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PageRevision',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField()),
                ('name', models.CharField(max_length=200, null=True)),
                ('version', models.IntegerField(default=1, editable=False)),
                ('time', models.DateTimeField(auto_now_add=True, null=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, null=True)),
                ('page', models.ForeignKey(to='pages.Page')),
            ],
            options={
                'ordering': ['-version'],
            },
            bases=(models.Model,),
        ),
    ]

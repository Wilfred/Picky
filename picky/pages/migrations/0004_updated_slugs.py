# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

from ..utils import slugify

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        for page in orm['pages.Page'].objects.all():
            page.name_slug = slugify(page.name)
            page.save()

    def backwards(self, orm):
        "Write your backwards methods here."
        # nothing to do

    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'name_lower': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'total_revisions': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'pages.pagerevision': {
            'Meta': {'ordering': "['-version']", 'object_name': 'PageRevision'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']"}),
            'time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['pages']
    symmetrical = True

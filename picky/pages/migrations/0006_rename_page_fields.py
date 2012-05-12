# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        db.rename_column('pages_page', 'is_latest_version', 'is_latest_revision')
        db.rename_column('pages_page', 'current_version_id', 'current_revision_id')

    def backwards(self, orm):
        db.rename_column('pages_page', 'is_latest_revision', 'is_latest_version')
        db.rename_column('pages_page', 'current_revision_id', 'current_version_id')

    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'current_revision': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_latest_revision': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_lower': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['pages']

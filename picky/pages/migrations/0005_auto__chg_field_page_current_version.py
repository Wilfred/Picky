# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Changing field 'Page.current_version'
        db.alter_column('pages_page', 'current_version_id',
                        self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page']))

    def backwards(self, orm):

        # Changing field 'Page.current_version'
        db.alter_column('pages_page', 'current_version_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'], null=True))

    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'current_version': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_latest_version': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_lower': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['pages']
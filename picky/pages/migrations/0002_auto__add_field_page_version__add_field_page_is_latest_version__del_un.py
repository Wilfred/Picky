# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Page', fields ['name']
        db.delete_unique('pages_page', ['name'])

        # Removing unique constraint on 'Page', fields ['name_slug']
        db.delete_unique('pages_page', ['name_slug'])

        # Adding field 'Page.version'
        db.add_column('pages_page', 'version',
                      self.gf('django.db.models.fields.IntegerField')(default=1),
                      keep_default=False)

        # Adding field 'Page.is_latest_version'
        db.add_column('pages_page', 'is_latest_version',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Page.version'
        db.delete_column('pages_page', 'version')

        # Deleting field 'Page.is_latest_version'
        db.delete_column('pages_page', 'is_latest_version')

        # Adding unique constraint on 'Page', fields ['name_slug']
        db.create_unique('pages_page', ['name_slug'])

        # Adding unique constraint on 'Page', fields ['name']
        db.create_unique('pages_page', ['name'])


    models = {
        'pages.page': {
            'Meta': {'object_name': 'Page'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_latest_version': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_lower': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'name_slug': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['pages']
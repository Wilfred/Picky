# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PageRevision'
        db.create_table('pages_pagerevision', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('content', self.gf('django.db.models.fields.TextField')()),
            ('page', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pages.Page'])),
            ('version', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('pages', ['PageRevision'])

        # Adding field 'Page.total_revisions'
        db.add_column('pages_page', 'total_revisions',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # save every page to create their first revision
        for page in orm.Page.objects.all():
            page.save()

    def backwards(self, orm):
        raise RuntimeError("You can't safely switch off versioning!")
        
        # Deleting model 'PageRevision'
        db.delete_table('pages_pagerevision')

        # Deleting field 'Page.total_revisions'
        db.delete_column('pages_page', 'total_revisions')


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
            'Meta': {'object_name': 'PageRevision'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'page': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pages.Page']"}),
            'version': ('django.db.models.fields.IntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['pages']

# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'FeedFile'
        db.create_table(u'aggregator_feedfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(unique=True, max_length=200)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('etag', self.gf('django.db.models.fields.CharField')(max_length=128, blank=True)),
            ('modified', self.gf('django.db.models.fields.CharField')(max_length=40, blank=True)),
        ))
        db.send_create_signal(u'aggregator', ['FeedFile'])

        # Adding model 'Feed'
        db.create_table(u'aggregator_feed', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed_file', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aggregator.FeedFile'], unique=True)),
            ('title', self.gf('django.db.models.fields.CharField')(default=None, max_length=512)),
            ('link', self.gf('django.db.models.fields.URLField')(default=None, max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')(default=None)),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('parsed_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'aggregator', ['Feed'])

        # Adding model 'Item'
        db.create_table(u'aggregator_item', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('feed', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['aggregator.Feed'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('link', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('content_source', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('link_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'aggregator', ['Item'])


    def backwards(self, orm):
        # Deleting model 'FeedFile'
        db.delete_table(u'aggregator_feedfile')

        # Deleting model 'Feed'
        db.delete_table(u'aggregator_feed')

        # Deleting model 'Item'
        db.delete_table(u'aggregator_item')


    models = {
        u'aggregator.feed': {
            'Meta': {'object_name': 'Feed'},
            'description': ('django.db.models.fields.TextField', [], {'default': 'None'}),
            'feed_file': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aggregator.FeedFile']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'default': 'None', 'max_length': '200'}),
            'parsed_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'aggregator.feedfile': {
            'Meta': {'object_name': 'FeedFile'},
            'body': ('django.db.models.fields.TextField', [], {}),
            'etag': ('django.db.models.fields.CharField', [], {'max_length': '128', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.CharField', [], {'max_length': '40', 'blank': 'True'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'unique': 'True', 'max_length': '200'})
        },
        u'aggregator.item': {
            'Meta': {'object_name': 'Item'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'content_source': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aggregator.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'link_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'taggit.tag': {
            'Meta': {'object_name': 'Tag'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '100'})
        },
        u'taggit.taggeditem': {
            'Meta': {'object_name': 'TaggedItem'},
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_tagged_items'", 'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'object_id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'tag': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "u'taggit_taggeditem_items'", 'to': u"orm['taggit.Tag']"})
        }
    }

    complete_apps = ['aggregator']
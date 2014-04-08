# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImportedArticle'
        db.create_table(u'article_importedarticle', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('teaser', self.gf('django.db.models.fields.TextField')()),
            ('feeditem', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['aggregator.FeedItem'], unique=True)),
            ('link_html', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'article', ['ImportedArticle'])


    def backwards(self, orm):
        # Deleting model 'ImportedArticle'
        db.delete_table(u'article_importedarticle')


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
        u'aggregator.feeditem': {
            'Meta': {'object_name': 'FeedItem'},
            u'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aggregator.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'link_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'article.importedarticle': {
            'Meta': {'object_name': 'ImportedArticle'},
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            'feeditem': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aggregator.FeedItem']", 'unique': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['article']
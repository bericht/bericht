# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Article.comments_count'
        db.add_column(u'article_article', u'comments_count',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Article.comments_count'
        db.delete_column(u'article_article', u'comments_count')


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
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'feed': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['aggregator.Feed']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'link_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'article.article': {
            'Meta': {'object_name': 'Article'},
            u'comments_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'content': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'published_at': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'teaser': ('django.db.models.fields.TextField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '512'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'article.importedarticle': {
            'Meta': {'object_name': 'ImportedArticle', '_ormbases': [u'article.Article']},
            u'article_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['article.Article']", 'unique': 'True', 'primary_key': 'True'}),
            'feeditem': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['aggregator.FeedItem']", 'unique': 'True'}),
            'link_html': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['article']
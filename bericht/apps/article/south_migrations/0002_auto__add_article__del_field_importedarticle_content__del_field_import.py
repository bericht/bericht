# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Article'
        db.create_table(u'article_article', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')()),
            ('updated_at', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('published_at', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=512)),
            ('content', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('teaser', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'article', ['Article'])

        # Deleting field 'ImportedArticle.content'
        db.delete_column(u'article_importedarticle', 'content')

        # Deleting field 'ImportedArticle.published_at'
        db.delete_column(u'article_importedarticle', 'published_at')

        # Deleting field 'ImportedArticle.title'
        db.delete_column(u'article_importedarticle', 'title')

        # Deleting field 'ImportedArticle.created_at'
        db.delete_column(u'article_importedarticle', 'created_at')

        # Deleting field 'ImportedArticle.teaser'
        db.delete_column(u'article_importedarticle', 'teaser')

        # Deleting field 'ImportedArticle.id'
        db.delete_column(u'article_importedarticle', u'id')

        # Deleting field 'ImportedArticle.updated_at'
        db.delete_column(u'article_importedarticle', 'updated_at')

        # Adding field 'ImportedArticle.article_ptr'
        db.add_column(u'article_importedarticle', u'article_ptr',
                      self.gf('django.db.models.fields.related.OneToOneField')(default=1, to=orm['article.Article'], unique=True, primary_key=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting model 'Article'
        db.delete_table(u'article_article')

        # Adding field 'ImportedArticle.content'
        db.add_column(u'article_importedarticle', 'content',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'ImportedArticle.published_at'
        db.add_column(u'article_importedarticle', 'published_at',
                      self.gf('django.db.models.fields.DateTimeField')(null=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImportedArticle.title'
        raise RuntimeError("Cannot reverse this migration. 'ImportedArticle.title' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ImportedArticle.title'
        db.add_column(u'article_importedarticle', 'title',
                      self.gf('django.db.models.fields.CharField')(max_length=512),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImportedArticle.created_at'
        raise RuntimeError("Cannot reverse this migration. 'ImportedArticle.created_at' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ImportedArticle.created_at'
        db.add_column(u'article_importedarticle', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImportedArticle.teaser'
        raise RuntimeError("Cannot reverse this migration. 'ImportedArticle.teaser' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ImportedArticle.teaser'
        db.add_column(u'article_importedarticle', 'teaser',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImportedArticle.id'
        raise RuntimeError("Cannot reverse this migration. 'ImportedArticle.id' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ImportedArticle.id'
        db.add_column(u'article_importedarticle', u'id',
                      self.gf('django.db.models.fields.AutoField')(primary_key=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'ImportedArticle.updated_at'
        raise RuntimeError("Cannot reverse this migration. 'ImportedArticle.updated_at' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'ImportedArticle.updated_at'
        db.add_column(u'article_importedarticle', 'updated_at',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True),
                      keep_default=False)

        # Deleting field 'ImportedArticle.article_ptr'
        db.delete_column(u'article_importedarticle', u'article_ptr_id')


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
        u'article.article': {
            'Meta': {'object_name': 'Article'},
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
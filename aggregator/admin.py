from django.contrib import admin
from .models import FeedFile, Feed, FeedItem


def fetch_feed(modeladmin, request, queryset):
    for obj in queryset:
        obj.fetch()
fetch_feed.short_description = "Fetch feed & update FeedItems"


class FeedFileAdmin(admin.ModelAdmin):
    fields = ('url',)
    list_display = ['url', 'updated_at']
    ordering = ['updated_at']
    actions = [fetch_feed]


class FeedAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed_file', 'link', 'parsed_at']
    ordering = ['parsed_at', 'feed_file']


class FeedItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'feed', 'link', 'updated_at']
    ordering = ['updated_at', 'feed', 'title']

admin.site.register(FeedFile, FeedFileAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(FeedItem, FeedItemAdmin)

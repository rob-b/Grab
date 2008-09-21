from feeds.models import Feed, Post
from django.contrib import admin

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'feed', 'updated')
    list_filter = ('feed',)

admin.site.register(Feed)
admin.site.register(Post, PostAdmin)

from django.contrib import admin
from .models import Post


class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'timestamp']
    list_display_links = ['timestamp']
    list_editable = ['title']
    list_filter = ['updated', 'timestamp']
    search_fields = ['title', 'content']
    model = Post


admin.site.register(Post, PostAdmin)

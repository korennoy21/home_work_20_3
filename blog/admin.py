from django.contrib import admin
from blog.models import BlogEntre

@admin.register(BlogEntre)
class BlogEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'publications', 'views')
    search_fields = ('title', 'publications')

from django.contrib import admin

from .models import Post, Like, User


admin.site.register(User)
admin.site.register(Like)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}

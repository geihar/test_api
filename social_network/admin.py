from django.contrib import admin

from .models import Post, Like, User


admin.site.register(User)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author")
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Like)
class PostAdmin(admin.ModelAdmin):
    list_display = ("post", "creation_date", "user")

from django.contrib import admin
from .models import Category, Post, Comment, Vote
from mptt.admin import MPTTModelAdmin

@admin.register(Post)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('title', 'id', 'status', 'author')

admin.site.register(Category)
admin.site.register(Vote)
admin.site.register(Comment, MPTTModelAdmin)
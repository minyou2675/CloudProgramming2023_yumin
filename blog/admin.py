from django.contrib import admin
from .models import Post, Category, Tag, Comment
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.
admin.site.register(Post, MarkdownxModelAdmin)

admin.site.register(Comment)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug' : ('name',)}
admin.site.register(Category)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields= {'slug' : ('name',)}
admin.site.register(Tag)
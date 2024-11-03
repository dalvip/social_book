from django.contrib import admin
from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'created_at', 'is_public')
    list_filter = ('is_public', 'created_at', 'genre')
    search_fields = ('title', 'author__username', 'description')
    date_hierarchy = 'created_at'

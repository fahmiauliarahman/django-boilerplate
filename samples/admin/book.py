from django.contrib import admin
from unfold.admin import ModelAdmin

from samples.models.book import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    pass

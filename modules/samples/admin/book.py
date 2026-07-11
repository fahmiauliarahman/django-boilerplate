from django.contrib import admin
from unfold.admin import ModelAdmin

from modules.samples.models.book import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    # We can control the fields to display by specifying them in a list_display property in the admin.py file.
    list_display = ("name", "slug", "published_date", "is_released")

    # Adds a sidebar on the right that allows users to filter the list view by specific fields.
    list_filter = ("is_released", "published_date")

    # Adds a search bar at the top, allowing users to search text fields (supports lookups like '__username').
    search_fields = ("name",)

    # Allows users to edit specific fields directly from the list view without clicking into the object.
    list_editable = ("is_released",)

    # Sets the default sorting order of the records in the list view (a minus prefix means descending).
    ordering = ("-published_date", "name")

    # Makes specific fields read-only on both the add and change pages (great for timestamps).
    readonly_fields = ("created_at", "updated_at", "slug")

    # Automatically fills in a field (like a URL slug) based on what the user types into another field.
    # prepopulated_fields = {"slug": ("name",)}

    # Controls how many items appear on each page of the list view before pagination links appear.
    list_per_page = 25

    # Replaces drop-down menus for ForeignKey fields with a searchable, high-performance input box.
    # autocomplete_fields = ()

    # Organizes the detail/edit form into distinct, visually separated sections with optional styling.
    fieldsets = (
        (
            "Core Content",
            {
                "fields": (
                    "name",
                    "photo",
                    "slug",
                )
            },
        ),
        (
            "Permissions & Dates",
            {
                # "classes": ("collapse", "wide",),  # Makes this section collapsible
                "fields": ("is_released", "published_date", "created_at"),
            },
        ),
    )

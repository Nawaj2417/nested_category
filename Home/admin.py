from django.contrib import admin
from .models import Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'parent', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name',)

    def get_queryset(self, request):
        # Include all categories in the queryset
        qs = super().get_queryset(request)
        return qs

    def delete_model(self, request, obj):
        # Soft delete instead of hard delete
        obj.is_deleted = True
        obj.save()

    def restore_categories(self, request, queryset):
        # Restore selected soft-deleted categories
        for category in queryset:
            category.is_deleted = False
            category.save()
        self.message_user(request, "Selected categories have been restored.")

    restore_categories.short_description = "Restore selected categories"

    actions = [restore_categories]  # Add the restore action

# Register the custom admin class
admin.site.register(Category, CategoryAdmin)

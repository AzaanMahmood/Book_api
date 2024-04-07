from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import  Book

class IsActiveFilter(admin.SimpleListFilter):
    title = _('Active Status')
    parameter_name = 'is_active'

    def lookups(self, request, model_admin):
        return (
            ('active', _('Active')),
            ('inactive', _('Inactive')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'active':
            return queryset.filter(is_active=True)
        elif self.value() == 'inactive':
            return queryset.filter(is_active=False)

class BookAdmin(admin.ModelAdmin):
    list_display=['id', 'title','author','publication_date','is_active']
    list_filter = [IsActiveFilter]

admin.site.register(Book, BookAdmin)

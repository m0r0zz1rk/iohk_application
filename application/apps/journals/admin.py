from django.contrib import admin

from apps.journals.models import Journal


@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    """Отображение журнала событий"""
    list_display = ('event_time', 'source', 'rec_type', 'description')

# Register your models here.

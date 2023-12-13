from django.contrib import admin

from apps.admins.models.guides.event_types import EventTypes


@admin.register(EventTypes)
class EventTypesAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'name')

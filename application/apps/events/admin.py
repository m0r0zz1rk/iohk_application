from django.contrib import admin

from apps.events.models import Events, EventTypes, EventForms, EventsInformation


@admin.register(Events)
class EventsAdmin(admin.ModelAdmin):
    list_display = ('name', 'event_type', 'date_start', 'date_end')


@admin.register(EventTypes)
class EventTypesAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'name')


@admin.register(EventForms)
class EventFormsAdmin(admin.ModelAdmin):
    list_display = ('object_id', 'name')


@admin.register(EventsInformation)
class EventsInformationAdmin(admin.ModelAdmin):
    pass

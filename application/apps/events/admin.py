from django.contrib import admin

from apps.events.models import Events, EventTypes, EventForms, EventsInformation, EventsSchedule, EventsAppsRequired


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


@admin.register(EventsSchedule)
class EventsScheduleAdmin(admin.ModelAdmin):
    pass


@admin.register(EventsAppsRequired)
class EventsAppsRequiredAdmin(admin.ModelAdmin):
    list_display = ('event', 'user_app_required', 'participant_app_required')

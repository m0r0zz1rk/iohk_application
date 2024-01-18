from django.contrib import admin

from apps.celery_app.models import UserEventEmails


@admin.register(UserEventEmails)
class UserEventEmailsAdmin(admin.ModelAdmin):
    list_display = ('user', 'event')

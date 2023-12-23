from django.contrib import admin

from apps.applications.models import AppFieldTypes, AppFields, FieldAvailableValues


@admin.register(AppFieldTypes)
class AppFieldTypesAdmin(admin.ModelAdmin):
    pass


@admin.register(AppFields)
class AppFieldsAdmin(admin.ModelAdmin):
    pass


@admin.register(FieldAvailableValues)
class FieldAvailableValuesAdmin(admin.ModelAdmin):
    pass

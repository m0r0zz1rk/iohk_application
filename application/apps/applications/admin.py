from django.contrib import admin

from apps.applications.models import AppFieldTypes, AppFields, FieldAvailableValues, Apps, AppFormFields


@admin.register(AppFieldTypes)
class AppFieldTypesAdmin(admin.ModelAdmin):
    list_display = ('alias', 'type')


@admin.register(AppFields)
class AppFieldsAdmin(admin.ModelAdmin):
    pass


@admin.register(FieldAvailableValues)
class FieldAvailableValuesAdmin(admin.ModelAdmin):
    pass


@admin.register(Apps)
class AppsAdmin(admin.ModelAdmin):
    list_display = ('profile', 'event', 'status')


@admin.register(AppFormFields)
class AppFormFieldsAdmin(admin.ModelAdmin):
    list_display = ('app', 'field_name', 'value')

    def field_name(self, obj):
        return obj.field.name

    field_name.short_description = 'Поле'

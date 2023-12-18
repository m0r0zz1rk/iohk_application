from django.contrib import admin

from apps.admins.models.guides.participant_categories import ParticipantCategories


@admin.register(ParticipantCategories)
class ParticipantCategoriesAdmin(admin.ModelAdmin):

    def user_role(self, obj):
        if obj.group is None:
            return '-'
        return obj.group.name

    user_role.short_description = 'Роль пользователей'

    list_display = ('object_id', 'name', 'user_role')


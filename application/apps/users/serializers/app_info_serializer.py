from rest_framework import serializers

from apps.applications.models import Apps


class AppInfoSerializer(serializers.ModelSerializer):
    """Сериализация основной информации о мероприятии"""

    event = serializers.SerializerMethodField(
        label='Информация о мероприятии'
    )

    def get_event(self, obj):
        return obj.event.__str__()

    class Meta:
        model = Apps
        exclude = ('profile',)
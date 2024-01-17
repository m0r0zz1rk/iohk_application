import datetime

from django.core.files.storage import default_storage
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets

from apps.commons.permissions.is_administrators import IsAdministrators
from apps.commons.permissions.is_auth import IsAuth
from apps.commons.serializers.tinymce_image_serializer import TinyMCEImageSerializer
from apps.commons.utils.django.django import DjangoUtils
from apps.commons.utils.django.response import ResponseUtils


class TinyMCEImagesUploadViewSet(viewsets.ViewSet):
    """Загрузка изображений в вопросах для TinyMCE"""
    permission_classes = [IsAuth, IsAdministrators]
    ru = ResponseUtils()

    @swagger_auto_schema(
        tags=['TinyMCE'],
        request_body=TinyMCEImageSerializer,
        operation_description="Загрузка изображений",
        responses={
            '400': 'Ошибка при загрузке изображения: (текст ошибки)',
            '401': 'Пользователь не авторизован',
            '403': 'Доступ запрещен',
            '200': 'Изображение успешно загружено',
        }
    )
    def image_upload(self, request, *args, **kwargs):
        """Загрузка изображений"""
        print(request)
        try:
            file = request.FILES.get('file')
        except BaseException:
            return self.ru.bad_request_response('Ошибка при получении файла. '
                                                'Повторите попытку или выберите другой файл')
        try:
            media_root = DjangoUtils().get_parameter_from_settings('MEDIA_ROOT')
            filename = (f'{media_root}/images/{request.data['name']}/'
                        f'{datetime.datetime.now().strftime("%d.%m.%Y")}.jpg')
            file_path = default_storage.save(filename, file)
            return self.ru.ok_response_dict({'location': f'/media/{file_path}'})
        except BaseException:
            return self.ru.bad_request_response('Произошла ошибка при сохранении файла, '
                                                'повторите попытку позже')

import datetime
import uuid
from typing import Optional

from apps.applications.models import Apps
from apps.authen.models import Profiles
from apps.authen.utils.profile import ProfileUtils
from apps.commons.consts.apps.app_statuses import APP_STATUSES, DRAFT, CREATED, SHIPPED, ACCEPTED, REJECTED, REVOKED, \
    COMPLETED


class AppsUtils:
    """Класс методов для работы с заявками"""

    @staticmethod
    def get_all_apps():
        """Получение всех заявок по всем мероприятиям"""
        return Apps.objects.all().order_by('-date_create')

    @staticmethod
    def get_user_apps_list(user_id: int) -> Optional[Apps]:
        """Получение списка заявок пользователя"""
        try:
            profile = ProfileUtils.get_profile_by_user_id(user_id)
            return Apps.objects.filter(profile_id=profile.object_id).order_by('-date_create')
        except Exception:
            return None

    @staticmethod
    def app_submit(profile_id: uuid, event_id: uuid) -> bool:
        """Подать заявку на участие в мероприятии"""
        try:
            if not Apps.objects.filter(profile_id=profile_id).filter(event_id=event_id).exists():
                new_app = Apps(
                    profile_id=profile_id,
                    event_id=event_id
                )
                new_app.save()
            return True
        except Exception:
            return False

    @staticmethod
    def get_app_by_user_and_event_id(user_id: int, event_id: uuid) -> Optional[Apps]:
        """Получение заявки по ID пользователя и Object_id мероприятия"""
        try:
            return Apps.objects.filter(
                profile_id=Profiles.objects.get(django_user_id=user_id).object_id
            ).get(event_id=event_id)
        except Exception:
            return None

    @staticmethod
    def get_app_by_object_id(app_id: uuid) -> Optional[Apps]:
        """Получение заявки по Object_id"""
        try:
            return Apps.objects.get(object_id=app_id)
        except Exception:
            return None

    @staticmethod
    def get_app_by_profile_and_event_id(profile_id: uuid, event_id: uuid) -> Optional[Apps]:
        """Получение заявки по object_id"""
        try:
            return Apps.objects.filter(profile_id=profile_id).get(event_id=event_id)
        except Exception:
            return None

    @staticmethod
    def check_event_app_for_user(profile_id: uuid, event_id: uuid) -> bool:
        """Проверка на наличие заявки у пользователя на участие в мероприятии"""
        try:
            return Apps.objects.filter(profile_id=profile_id).filter(event_id=event_id).exists()
        except Exception:
            return False

    @staticmethod
    def change_app_status(
            app_id: uuid,
            new_status: APP_STATUSES,
            message=None,
            result=None
    ) -> bool:
        """Изменение статуса заявки"""
        try:
            app = Apps.objects.get(object_id=app_id)
            app.date_update = datetime.date.today()
            match new_status:
                case 'DRAFT':
                    return False

                case 'CREATED':
                    if app.status in [DRAFT, CREATED, REJECTED, REVOKED]:
                        app.status = CREATED

                case 'SHIPPED':
                    if app.status == CREATED:
                        app.status = SHIPPED

                case 'ACCEPTED' | 'REJECTED':
                    if app.status in [SHIPPED, COMPLETED]:
                        app.status = new_status

                case 'REVOKED':
                    app.status = REVOKED

                case 'COMPLETED':
                    if app.status in [ACCEPTED, COMPLETED]:
                        app.status = COMPLETED

                case _:
                    return False
            if message is not None:
                app.message = message
            if result is not None:
                app.result = result
            app.save()
            return True
        except Exception:
            return False

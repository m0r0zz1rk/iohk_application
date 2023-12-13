import datetime
from typing import Optional


class DateUtils:
    """Валидаторы и методы для даты/даты и времени"""

    @staticmethod
    def is_object_date(obj) -> bool:
        """Проверка является ли объект датой"""
        return isinstance(obj, datetime.datetime)

    @staticmethod
    def convert_str_to_date(date: str):
        """Преобразование строковой даты ДД-ММ-ГГГГ в python datetime"""
        try:
            return datetime.datetime.strptime(date, '%d.%m.%Y')
        except BaseException:
            return None

    @staticmethod
    def convert_date_to_str(date: datetime.date) -> str:
        """Преобразование даты в строку формата: дд.мм.гггг"""
        if date is not None:
            return date.strftime("%d.%m.%Y")
        return None

    @staticmethod
    def convert_datetime_to_str(date: datetime.datetime) -> Optional[str]:
        """Преобразование даты в строку формата: дд.мм.гггг"""
        if date is not None:
            return date.strftime("%d.%m.%Y %H:%m")
        return None

    def convert_obj_to_date(self, obj):
        if self.is_object_date(obj):
            return obj.strftime("%d.%m.%Y")
        else:
            try:
                return datetime.date(obj).strftime("%d.%m.%Y")
            except:
                return None

    @staticmethod
    def convert_html_date(obj) -> Optional[datetime.date]:
        """Конвертирование даты с HTML формы в дату для python"""
        try:
            return datetime.datetime.strptime(obj, '%Y-%m-%d')
        except BaseException:
            try:
                return datetime.datetime.strptime(obj, '%d.%m.%Y')
            except BaseException:
                return None

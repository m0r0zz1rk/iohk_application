from typing import Optional

from django.apps import apps

from apps.events.utils.events import EventsUtils


class CountReportUtils:
    """Класс методов для работы с количественным отчетом"""

    apps_model = apps.get_model('applications', 'Apps')
    app_fields_model = apps.get_model('applications', 'AppFields')
    app_form_fields_model = apps.get_model('applications', 'AppFormFields')
    events = filters = total_row_list = []
    apps_types = 'all'
    total_row = False

    def __init__(self, events: list, filters: list, apps_types: str, total_row: bool):
        """
            Инициализация класса
        :param events: список object_id мероприятий
        :param filters: список фильтров
        :param apps_types: тип заявок (all, user, part)
        :param total_row: Необходимость итоговой строки
        """
        self.events = events
        self.filters = filters
        self.apps_types = apps_types
        self.total_row = total_row
        self._generate_total_row_list()

    def _generate_total_row_list(self):
        """Генерация списка общих значений по фильтрам для итоговой строки"""
        for f in self.filters:
            self.total_row_list.append(
                {
                    'filter_id': f['id'],
                    'count': 0
                }
            )
        self.total_row_list.append(
            {
                'filter_id': 'total',
                'count': 0
            }
        )

    def add_to_total_row_list(self, filter_id, count: int):
        """Добавление количества заявок в список общих значений"""
        for rec in self.total_row_list:
            if rec['filter_id'] == filter_id:
                rec['count'] += count

    def get_count_from_total_row_list(self, filter_id) -> int:
        """Получение количества заявок из списка общих значений"""
        for rec in self.total_row_list:
            if rec['filter_id'] == filter_id:
                return rec['count']

    def _header_row(self) -> list:
        """Получение строки заголовка для страницы количественного отчета"""
        header_row = [
            {
                'row': 1,
                'col': 1,
                'value': 'Мероприятие\Фильтры',
                'bold': True,
                'width': 100,
                'align_center': True,
                'merge': '2:::1'
            }
        ]
        if len(self.filters) > 0:
            header_row.append({
                'row': 1,
                'col': 2,
                'value': 'Поле',
                'bold': True,
                'width': 30,
                'align_center': True,
            })
            header_row.append({
                'row': 2,
                'col': 2,
                'value': 'Значение',
                'bold': True,
                'width': 30,
                'align_center': True,
            })
        for filter_index, filter in enumerate(self.filters, start=1):
            header_row.append({
                'row': 1,
                'col': 2 + filter_index,
                'value': filter['field'],
                'bold': True,
                'width': 30,
                'align_center':True
            })
            header_row.append({
                'row': 2,
                'col': 2 + filter_index,
                'value': filter['value'],
                'bold': True,
                'width': 30,
                'align_center': True
            })
        header_row.append({
            'row': 1,
            'col': 3 + len(self.filters),
            'value': 'Всего',
            'bold': True,
            'width': 30,
            'align_center': True,
            'merge': f'2:::{3+len(self.filters)}'
        })
        return header_row

    def content_data(self) -> Optional[list]:
        """Заполнение листа отчета данными"""
        #try:
        excel = []
        content = self._header_row()
        event_ids = [rec['event_id'] for rec in self.events]
        form_fields = (self.app_form_fields_model.objects.
                       select_related('field').filter(app__event_id__in=event_ids))
        match self.apps_types:
            case 'user':
                form_fields = form_fields.filter(field__user_app=True)
            case 'part':
                form_fields = form_fields.filter(field__user_app=False)
        for index, event_id in enumerate(event_ids, start=1):
            no_apps = False
            applications = self.apps_model.objects.filter(event_id=event_id)
            apps_count = applications.count()
            if apps_count == 0:
                no_apps = True
            content.append({
                'row': 2 + index,
                'col': 1,
                'value': EventsUtils().get_event_display_name(event_id),
                'width': 100,
                'align_center': True,
                'merge': f'{2+index}:::2'
            })
            for f_id, f in enumerate(self.filters, start=1):
                if no_apps:
                    filter_count = 0
                else:
                    filter_count = (form_fields.filter(app__in=applications).
                                    filter(field__name=f['field']).
                                    filter(value__contains=f['value']).count())
                content.append({
                    'row': 2 + index,
                    'col': 2 + f_id,
                    'value': filter_count,
                    'width': 30,
                    'align_center': True,
                })
                self.add_to_total_row_list(f['id'], filter_count)
            content.append({
                'row': 2 + index,
                'col': 3 + len(self.filters),
                'value': apps_count,
                'width': 30,
                'align_center': True
            })
            self.add_to_total_row_list('total', apps_count)
        print(self.total_row_list)
        if self.total_row:
            content.append({
                'row': 3 + len(event_ids),
                'col': 1,
                'value': 'Итого',
                'bold': True,
                'width': 30,
                'align_center': True,
                'merge': f'{3 + len(event_ids)}:::2'
            })
            for f_id, f in enumerate(self.filters, start=1):
                content.append({
                    'row': 3 + len(event_ids),
                    'col': 2 + f_id,
                    'value': self.get_count_from_total_row_list(f['id']),
                    'bold': True,
                    'width': 30,
                    'align_center': True
                })
            content.append({
                'row': 3 + len(event_ids),
                'col': 3 + len(self.filters),
                'value': self.get_count_from_total_row_list('total'),
                'bold': True,
                'width': 30,
                'align_center': True
            })
        title = 'Все заявки'
        match self.apps_types:
            case 'user':
                title = 'Пользователи'
            case 'part':
                title = 'Участники'
        excel.append({
            'title': title,
            'sheet_data': content
        })
        return excel
        #except Exception:
        #    return None

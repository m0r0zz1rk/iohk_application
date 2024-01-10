from django.urls import path

from apps.users.api.apps.app_form_fields_viewset import AppFormFieldsViewSet
from apps.users.api.apps.apps_viewset import AppsViewSet
from apps.users.api.events.event_app_required_viewset import EventAppRequiredViewSet
from apps.users.api.events.event_information_viewset import EventInformationViewSet
from apps.users.api.events.event_schedule_viewset import EventScheduleViewSet
from apps.users.api.events.events_types_viewset import EventsTypesViewSet
from apps.users.api.events.events_viewset import EventsViewSet

event_types_urlpatterns = [
    path('event_types/', EventsTypesViewSet.as_view({'get': 'list'}))
]

events_urlpatterns = [
    path('events/', EventsViewSet.as_view({'get': 'list'}))
]

event_info_urlpatterns = [
    path('event_info/<uuid:event_id>/', EventInformationViewSet.as_view({'get': 'retrieve'}))
]

events_schedule_urlpatterns = [
    path('event_schedule/<uuid:event_id>/', EventScheduleViewSet.as_view({'get': 'list'})),
]

event_app_required_urlpatterns = [
    path('event_app_required/<uuid:event_id>/', EventAppRequiredViewSet.as_view({'get': 'get_app_required'}))
]

apps_urlpatterns = [
    path('apps/check_exist/<uuid:event_id>/', AppsViewSet.as_view({'get': 'check_app_exist'})),
    path('apps/app_info/<uuid:event_id>/', AppsViewSet.as_view({'get': 'get_app_info'})),
    path('apps/user_app_fields/<uuid:event_id>/', AppsViewSet.as_view({'get': 'get_app_fields'})),
    path('apps/save/', AppsViewSet.as_view({'post': 'save_app'})),
    path('apps/status_change/', AppsViewSet.as_view({'post': 'app_status_change'})),
]

app_form_fields_urlpatterns = [
    path('app_form_fields/save/', AppFormFieldsViewSet.as_view({'post': 'save_field_value'})),
    path('app_form_fields/part/<uuid:event_id>/', AppFormFieldsViewSet.as_view({'get': 'get_part_app_fields'})),
    path('app_form_fields/part_recs/<uuid:event_id>/', AppFormFieldsViewSet.as_view({'get': 'get_part_app_recs'})),
    path('app_form_fields/part_app_save/<uuid:event_id>/', AppFormFieldsViewSet.as_view({'post': 'save_part_app_rec'})),
    path('app_form_fields/part_app_edit/<uuid:event_id>/', AppFormFieldsViewSet.as_view({'patch': 'edit_part_app_rec'})),
    path('app_form_fields/part_app_delete/', AppFormFieldsViewSet.as_view({'delete': 'delete_part_app_rec'})),
]

urlpatterns = (event_types_urlpatterns +
               event_app_required_urlpatterns +
               events_urlpatterns +
               event_info_urlpatterns +
               events_schedule_urlpatterns +
               apps_urlpatterns +
               app_form_fields_urlpatterns)

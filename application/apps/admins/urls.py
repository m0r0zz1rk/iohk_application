from django.urls import path

from apps.admins.api.apps.admin_apps_list_viewset import AdminAppsListViewSet
from apps.admins.api.apps.admin_apps_viewset import AdminAppsViewSet
from apps.admins.api.events.event_app_fields_viewset import EventAppFieldsViewSet
from apps.admins.api.events.events_app_required_viewset import EventsAppRequiredViewSet
from apps.admins.api.events.events_information_viewset import EventsInformationViewSet
from apps.admins.api.events.events_schedule_viewset import EventsScheduleViewSet
from apps.admins.api.events.events_viewset import EventsViewSet
from apps.admins.api.guides.events_forms_viewset import EventsFormsViewSet
from apps.admins.api.guides.events_types_viewset import EventsTypesViewSet
from apps.admins.api.guides.participant_categories_viewset import ParticipantCategoriesViewSet
from apps.admins.api.journal_viewset import JournalViewSet
from apps.admins.api.main_viewset import MainViewSet
from apps.admins.api.users_viewset import UsersViewSet

guides_urlpatterns = [
    path('events_types/', EventsTypesViewSet.as_view({'get': 'list'})),
    path('events_type_new/', EventsTypesViewSet.as_view({'post': 'save'})),
    path('events_type_edit/<uuid:object_id>/', EventsTypesViewSet.as_view({'patch': 'edit'})),
    path('events_type_delete/<uuid:object_id>/', EventsTypesViewSet.as_view({'delete': 'delete'})),

    path('participant_categories/', ParticipantCategoriesViewSet.as_view({'get': 'list'})),
    path('participant_category_new/', ParticipantCategoriesViewSet.as_view({'post': 'save'})),
    path('participant_category_edit/<uuid:object_id>/', ParticipantCategoriesViewSet.as_view({'patch': 'edit'})),
    path('participant_category_delete/<uuid:object_id>/', ParticipantCategoriesViewSet.as_view({'delete': 'delete'})),

    path('events_forms/', EventsFormsViewSet.as_view({'get': 'list'})),
    path('events_form_new/', EventsFormsViewSet.as_view({'post': 'save'})),
    path('events_form_edit/<uuid:object_id>/', EventsFormsViewSet.as_view({'patch': 'edit'})),
    path('events_form_delete/<uuid:object_id>/', EventsFormsViewSet.as_view({'delete': 'delete'})),
]

users_urlpatterns = [
    path('users/', UsersViewSet.as_view({'get': 'list'})),
    path('user_check_email/', UsersViewSet.as_view({'post': 'check_change_email'})),
    path('user_check_phone/', UsersViewSet.as_view({'post': 'check_change_phone'})),
    path('user_edit/', UsersViewSet.as_view({'post': 'edit'})),
    path('user_change_password/', UsersViewSet.as_view({'post': 'change_user_password'})),
]

journal_urlpatterns = [
    path('journal/', JournalViewSet.as_view({'get': 'list'}))
]

events_urlpatterns = [
    path('events/', EventsViewSet.as_view({'get': 'list'})),
    path('event/<uuid:event_id>/', EventsViewSet.as_view({'get': 'retrieve'})),
    path('event_new/', EventsViewSet.as_view({'post': 'save'})),
    path('event_edit/<uuid:object_id>/', EventsViewSet.as_view({'patch': 'edit'})),
    path('event_delete/<uuid:object_id>/', EventsViewSet.as_view({'delete': 'delete'})),
]

events_information_urlpatterns = [
    path('information/', EventsInformationViewSet.as_view({'get': 'list'})),
    path('information_save/<uuid:event_id>/', EventsInformationViewSet.as_view({'patch': 'save'})),
]

events_schedule_urlpatterns = [
    path('schedule/<uuid:event_id>/', EventsScheduleViewSet.as_view({'get': 'list'})),
    path('schedule_add/<uuid:event_id>/', EventsScheduleViewSet.as_view({'post': 'save'})),
    path('schedule_edit/<uuid:schedule_id>/', EventsScheduleViewSet.as_view({'patch': 'edit'})),
    path('schedule_delete/<uuid:schedule_id>/', EventsScheduleViewSet.as_view({'delete': 'delete'})),
]

events_apps_required_urlpatterns = [
    path('apps_required/<uuid:event_id>/', EventsAppRequiredViewSet.as_view({'get': 'list'})),
    path('apps_required_edit/', EventsAppRequiredViewSet.as_view({'post': 'edit'})),
]

event_app_fields_urlpatterns = [
    path('app_fields/<uuid:event_id>/<str:app_type>/', EventAppFieldsViewSet.as_view({'get': 'list'})),
    path('app_field_new/', EventAppFieldsViewSet.as_view({'post': 'save'})),
    path('app_field_edit/<uuid:field_id>/', EventAppFieldsViewSet.as_view({'patch': 'edit'})),
    path('app_field_delete/<uuid:field_id>/', EventAppFieldsViewSet.as_view({'delete': 'delete'})),
]

apps_urlpatterns = [
    path('apps/list/', AdminAppsListViewSet.as_view({'get': 'get_apps_list'})),
    path('apps/app_info/<uuid:app_id>/', AdminAppsViewSet.as_view({'get': 'get_app_info'})),
    path('apps/user_app_fields/<uuid:app_id>/', AdminAppsViewSet.as_view({'get': 'get_app_fields'})),
    path('apps/part_form_fields/<uuid:app_id>/', AdminAppsViewSet.as_view({'get': 'get_part_app_fields'})),
    path('apps/part_form_recs/<uuid:app_id>/', AdminAppsViewSet.as_view({'get': 'get_part_app_recs'})),
]

main_urlpatterns = [
    path('main/apps_count/', MainViewSet.as_view({'get': 'get_app_count_for_published_events'}))
]

urlpatterns = guides_urlpatterns + users_urlpatterns + journal_urlpatterns + \
            events_urlpatterns + events_information_urlpatterns + \
            events_schedule_urlpatterns + events_apps_required_urlpatterns + \
            event_app_fields_urlpatterns + apps_urlpatterns + main_urlpatterns

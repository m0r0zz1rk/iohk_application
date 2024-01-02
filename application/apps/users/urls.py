from django.urls import path

from apps.users.api.apps.apps_viewset import AppsViewSet
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

apps_urlpatterns = [
    path('apps/check_exist/<uuid:event_id>/', AppsViewSet.as_view({'get': 'check_app_exist'})),
    path('apps/app_info/<uuid:event_id>/', AppsViewSet.as_view({'get': 'get_app_info'})),
    path('apps/app_user_fields/<uuid:event_id>/', AppsViewSet.as_view({'get': 'get_user_app_fields'})),
]

urlpatterns = event_types_urlpatterns + events_urlpatterns + event_info_urlpatterns + events_schedule_urlpatterns + \
    apps_urlpatterns

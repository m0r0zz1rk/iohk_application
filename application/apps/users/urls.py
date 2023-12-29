from django.urls import path

from apps.users.api.events_types_viewset import EventsTypesViewSet
from apps.users.api.events_viewset import EventsViewSet

event_types_urlpatterns = [
    path('event_types/', EventsTypesViewSet.as_view({'get': 'list'}))
]

events_urlpatterns = [
    path('events/', EventsViewSet.as_view({'get': 'list'}))
]

urlpatterns = event_types_urlpatterns + events_urlpatterns

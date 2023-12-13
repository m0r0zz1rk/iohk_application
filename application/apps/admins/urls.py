from django.urls import path

from apps.admins.api.guides.events_types_viewset import EventsTypesViewSet

guides_urlpatterns = [
    path('events_types_count/', EventsTypesViewSet.as_view({'get': 'count'})),
    path('events_types/', EventsTypesViewSet.as_view({'get': 'list'})),
    path('events_type_new/', EventsTypesViewSet.as_view({'post': 'save'})),
    path('events_type_edit/<uuid:object_id>/', EventsTypesViewSet.as_view({'patch': 'edit'})),
    path('events_type_delete/<uuid:object_id>/', EventsTypesViewSet.as_view({'delete': 'delete'})),
]

urlpatterns = guides_urlpatterns

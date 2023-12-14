from django.urls import path

from apps.admins.api.guides.events_forms_viewset import EventsFormsViewSet
from apps.admins.api.guides.events_types_viewset import EventsTypesViewSet
from apps.admins.api.guides.participant_categories_viewset import ParticipantCategoriesViewSet
from apps.admins.api.users.users_viewset import UsersViewSet

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
]

urlpatterns = guides_urlpatterns + users_urlpatterns

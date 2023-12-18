from django.urls import path

from apps.admins.api.events_information_viewset import EventsInformationViewSet
from apps.admins.api.events_viewset import EventsViewSet
from apps.admins.api.guides.events_forms_viewset import EventsFormsViewSet
from apps.admins.api.guides.events_types_viewset import EventsTypesViewSet
from apps.admins.api.guides.participant_categories_viewset import ParticipantCategoriesViewSet
from apps.admins.api.journal_viewset import JournalViewSet
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
    path('event_new/', EventsViewSet.as_view({'post': 'save'})),
    path('event_edit/<uuid:object_id>/', EventsViewSet.as_view({'patch': 'edit'})),
    path('event_delete/<uuid:object_id>/', EventsViewSet.as_view({'delete': 'delete'})),
]

events_information_urlpatterns = [
    path('information/', EventsInformationViewSet.as_view({'get': 'list'})),
    path('information_save/<uuid:event_id>/', EventsInformationViewSet.as_view({'patch': 'save'})),
]

urlpatterns = guides_urlpatterns + users_urlpatterns + journal_urlpatterns + \
            events_urlpatterns + events_information_urlpatterns

from django.urls import path

from apps.applications.api.app_field_types_viewset import AppFieldTypesViewSet
from apps.applications.api.field_available_values_viewset import FieldAvailableValuesViewSet

app_field_types_urlpatterns = [
    path('app_field_types/', AppFieldTypesViewSet.as_view({'get': 'list'}))
]

field_available_values_urlpatterns = [
    path('available_values/<uuid:field_id>/', FieldAvailableValuesViewSet.as_view({'get': 'list'})),
    path('available_value_add/<uuid:field_id>/', FieldAvailableValuesViewSet.as_view({'post': 'save'})),
    path('available_value_edit/<uuid:value_id>/', FieldAvailableValuesViewSet.as_view({'patch': 'edit'})),
    path('available_value_delete/<uuid:value_id>/', FieldAvailableValuesViewSet.as_view({'delete': 'delete'})),
]

urlpatterns = app_field_types_urlpatterns + field_available_values_urlpatterns

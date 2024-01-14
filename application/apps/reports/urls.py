from django.urls import path

from apps.reports.api.apps_report_viewset import AppsReportViewSet
from apps.reports.api.reports_events_viewset import ReportsEventsViewSet

events_urlpatterns = [
    path('events/list/', ReportsEventsViewSet.as_view({'get': 'list'}))
]

apps_report_urlpatterns = [
    path('apps_report/', AppsReportViewSet.as_view({'post': 'apps_report'})),
]

urlpatterns = events_urlpatterns + apps_report_urlpatterns

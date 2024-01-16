from django.urls import path

from apps.reports.api.apps_report_viewset import AppsReportViewSet
from apps.reports.api.count_report_viewset import CountReportViewSet
from apps.reports.api.reports_events_viewset import ReportsEventsViewSet

events_urlpatterns = [
    path('events/list/', ReportsEventsViewSet.as_view({'get': 'list'}))
]

reports_urlpatterns = [
    path('apps_report/', AppsReportViewSet.as_view({'post': 'apps_report'})),
    path('count_report/', CountReportViewSet.as_view({'post': 'count_report'})),
]

urlpatterns = events_urlpatterns + reports_urlpatterns

from django.urls import path
from .views import GoogleCalendarInitView, GoogleCalendarRedirectView
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('init/', GoogleCalendarInitView.as_view(), name='google_calendar_init'),
    path('redirect/', GoogleCalendarRedirectView.as_view(), name='google_calendar_redirect'),
    path('admin/', admin.site.urls),
    path('rest/v1/calendar/', include('calendar_integration.urls')),
]

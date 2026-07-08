from django.urls import path
from .views import SecurityLogListView

urlpatterns = [
    path("", SecurityLogListView.as_view(), name="security-log-list"),
]

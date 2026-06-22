from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

    # Home Page -> Employee List
    path(
        '',
        RedirectView.as_view(
            url='/employees/',
            permanent=False
        ),
        name='home'
    ),

    # Admin
    path(
        'admin/',
        admin.site.urls
    ),

    # Employees App
    path(
        'employees/',
        include('employees.urls')
    ),
]

# Media Files
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
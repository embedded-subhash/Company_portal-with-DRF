from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

urlpatterns = [

    path(
        '',
        RedirectView.as_view(
            url='/accounts/login/',
            permanent=False
        ),
        name='home'
    ),

    path(
        'admin/',
        admin.site.urls
    ),

    path(
        'accounts/',
        include('accounts.urls')
    ),

    path(
        'employees/',
        include('employees.urls')
    ),

    path(
       'departments/',
        include('departments.urls')
    ),
    path('api/',
          include('api.urls')
    ),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
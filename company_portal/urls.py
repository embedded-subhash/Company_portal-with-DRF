from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
schema_view = get_schema_view(

    openapi.Info(
        title="Company Portal API",
        default_version='v1',
        description="HR Management System APIs",
        contact=openapi.Contact(
            email="Subash@blackroth.in"
        ),
    ),

    public=True,
    permission_classes=[permissions.AllowAny],
)
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
    path(
    'swagger/',
    schema_view.with_ui(
        'swagger',
        cache_timeout=0
    ),
    name='schema-swagger-ui'
),

path(
    'redoc/',
    schema_view.with_ui(
        'redoc',
        cache_timeout=0
    ),
    name='schema-redoc'
),
    
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
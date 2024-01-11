from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from elections import urls as electionurls
from user_management import urls as userurls


# Create a router and register your viewsets with it.

electionurls_schema_view = get_schema_view(
    openapi.Info(
        title="SIGEF Backend API",
        default_version='v1',
        description="API for SIGEF Backend",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    patterns=electionurls.router.urls,  # Include router URLs in the schema view
)

user_schema_view = get_schema_view(
    openapi.Info(
        title="SIGEF Backend API",
        default_version='v1',
        description="API for SIGEF Backend",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    patterns=userurls.router.urls,  # Include router URLs in the schema view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(electionurls)),
    path('api/', include(userurls)),
    path('swagger/', electionurls_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('swagger/', user_schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', electionurls_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('redoc/', user_schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from elections.views import *
from user_management.views import CustomUserViewSet, CustomTokenObtainPairView

# Create a router and register your viewsets with it.
router = SimpleRouter()
router.register(r'institutions', InstitutionViewSet, basename='institutions')
router.register(r'campuses', CampusViewSet, basename='campuses')
router.register(r'faculties', FacultyViewSet, basename='faculties')
router.register(r'people', PersonViewSet, basename='people')
router.register(r'elections', ElectionViewSet, basename='elections')
router.register(r'candidates', CandidateViewSet, basename='candidates')
router.register(r'elector-registries', ElectorRegistryViewSet, basename='elector-registries')
router.register(r'user', CustomUserViewSet, basename='user')

schema_view = get_schema_view(
    openapi.Info(
        title="SIGEF Backend API",
        default_version='v1',
        description="API for SIGEF Backend",
        terms_of_service="https://www.yourapp.com/terms/",
        contact=openapi.Contact(email="contact@yourapp.com"),
        license=openapi.License(name="Your License"),
    ),
    public=True,
    patterns=router.urls,  # Include router URLs in the schema view
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

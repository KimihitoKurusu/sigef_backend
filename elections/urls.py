from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'institutions', InstitutionViewSet)
router.register(r'campuses', CampusViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'people', PersonViewSet)
router.register(r'elections', ElectionViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'elector-registries', ElectorRegistryViewSet)
router.register(r'candidate-log', CandidateLogViewSet)

urlpatterns = [
    path('elections/', include(router.urls)),
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter, Route
from .views import *
# Crea una nueva clase de router que extienda DefaultRouter
class CustomRouter(DefaultRouter):
    def get_routes(self, viewset):
        """
        Añade una ruta adicional para el método personalizado 'vote'.
        """
        routes = super().get_routes(viewset)
        custom_routes = [
            # Definir la ruta para el método 'vote'
            Route(
                url=r'^{prefix}/{lookup}{trailing_slash}vote/$',
                mapping={'post': 'vote'},
                name='{basename}-vote',
                detail=True,
                initkwargs={'suffix': 'Vote'}
            ),
        ]
        return routes + custom_routes

# Crea una instancia de tu nuevo router personalizado
router = CustomRouter()

router.register(r'institutions', InstitutionViewSet)
router.register(r'campuses', CampusViewSet)
router.register(r'faculties', FacultyViewSet)
router.register(r'people', PersonViewSet)
router.register(r'elections', ElectionViewSet)
router.register(r'candidates', CandidateViewSet)
router.register(r'elector-registries', ElectorRegistryViewSet)

urlpatterns = [
    path('elections/', include(router.urls)),
]

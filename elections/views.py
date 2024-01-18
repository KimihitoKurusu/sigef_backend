from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .permissions import IsCandidateManagerOrReadOnly
from .permissions import IsSuperUserOrReadOnly
from .serializers import *


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsSuperUserOrReadOnly]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer

    def update(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            return Response(serializer.data)
        except Exception as e:
            print(f"Error updating Person: {e}")
            return Response({"error": "Error updating Person"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsSuperUserOrReadOnly]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsCandidateManagerOrReadOnly]


class ElectorRegistryViewSet(viewsets.ModelViewSet):
    queryset = ElectorRegistry.objects.all()
    serializer_class = ElectorRegistrySerializer

    @action(detail=True, methods=['post'])
    def vote(self, request, pk=None):
        elector_registry = self.get_object()
        # Aquí debes agregar la lógica para manejar la votación
        # Puedes acceder a la instancia del ElectorRegistry mediante 'elector_registry'
        # y al cuerpo de la solicitud mediante 'request.data'

        # Por ejemplo, puedes actualizar el modelo y guardar los cambios
        # elector_registry.voted = True
        # elector_registry.save()

        # Retorna una respuesta adecuada según tus necesidades
        return Response({'message': 'Votación realizada con éxito'}, status=status.HTTP_200_OK)

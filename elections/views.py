from rest_framework import viewsets

from .permissions import IsCandidateManagerOrReadOnly, IsElectionManagerOrReadOnly
from .permissions import IsFacultyManagerOrReadOnly
from .permissions import IsInstitutionManagerOrReadOnly, IsCampusManagerOrReadOnly
from .serializers import *


class InstitutionViewSet(viewsets.ModelViewSet):
    queryset = Institution.objects.all()
    serializer_class = InstitutionSerializer
    permission_classes = [IsInstitutionManagerOrReadOnly]


class CampusViewSet(viewsets.ModelViewSet):
    queryset = Campus.objects.all()
    serializer_class = CampusSerializer
    permission_classes = [IsCampusManagerOrReadOnly]


class FacultyViewSet(viewsets.ModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsFacultyManagerOrReadOnly]


class PersonViewSet(viewsets.ModelViewSet):
    queryset = Person.objects.all()
    serializer_class = PersonSerializer


class ElectionViewSet(viewsets.ModelViewSet):
    queryset = Election.objects.all()
    serializer_class = ElectionSerializer
    permission_classes = [IsElectionManagerOrReadOnly]


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = Candidate.objects.all()
    serializer_class = CandidateSerializer
    permission_classes = [IsCandidateManagerOrReadOnly]


class ElectorRegistryViewSet(viewsets.ModelViewSet):
    queryset = ElectorRegistry.objects.all()
    serializer_class = ElectorRegistrySerializer

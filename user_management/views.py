from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import CustomUser, CustomUserLog
from .serializers import CustomUserSerializer, CustomUserLogSerializer
from .permissions import IsUserManager


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsUserManager]


class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = CustomUser.objects.get(username=request.data['username'])
        response.data['user_id'] = user.id
        response.data['username'] = user.username
        return response

class CustomUserLogViewSet(viewsets.ModelViewSet):
    queryset = CustomUserLog.objects.all()
    serializer_class = CustomUserLogSerializer
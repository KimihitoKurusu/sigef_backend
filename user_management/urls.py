# urls.py

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CustomTokenObtainPairView
from .views import CustomUserViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')

urlpatterns = [
    path('user/', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]

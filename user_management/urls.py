# urls.py

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomTokenObtainPairView
from .views import CustomUserViewSet, CustomUserLogViewSet

router = DefaultRouter()
router.register(r'users', CustomUserViewSet, basename='user')
router.register(r'user-log', CustomUserLogViewSet)

urlpatterns = [
    path('user/', include(router.urls)),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

]

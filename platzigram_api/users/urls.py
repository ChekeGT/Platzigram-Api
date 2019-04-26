"""Users app urls."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Viewsets
from .views import UserModelViewset

# Views
from rest_framework_simplejwt.views import TokenObtainPairView

router = SimpleRouter()

router.register(
    r'users',
    viewset=UserModelViewset,
    base_name='users'
)

app_name = 'Users'

urlpatterns = [
    path('users/login/', TokenObtainPairView.as_view(), name='users-login'),
    path('', include(router.urls)),
]

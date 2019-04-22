"""Users app urls."""

# Django
from django.urls import include, path

# Django REST Framework
from rest_framework.routers import SimpleRouter

# Viewsets
from .views import UserModelViewset

router = SimpleRouter()

router.register(
    r'',
    viewset=UserModelViewset,
    base_name='users'
)

app_name = 'Users'

urlpatterns = [
    path('', include(router.urls))
]

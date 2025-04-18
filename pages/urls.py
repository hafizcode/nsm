from django.urls import path
from .views import public_resources

urlpatterns = [
    path('', public_resources, name='public_resources'),
]

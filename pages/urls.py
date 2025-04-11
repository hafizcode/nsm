from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='public_home'),
    path('resources/', views.public_files, name='public_files'),  # 👈 Add this
]

from django.urls import path
from . import views
from core import views as core_views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('resources/', views.public_resources, name='public_resources'),
    path('login/', core_views.login_view, name='login'),

    path('groups/', views.group_list_view, name='group_list'),
    path('groups/<int:group_id>/', views.group_detail_view, name='group_detail'),
]

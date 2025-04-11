from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.staff_register, name='staff_register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_file, name='upload_file'),
    path('files/', views.file_list, name='file_list'),
    path('files/edit/<int:file_id>/', views.edit_file, name='edit_file'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),
    path('profile/', views.staff_profile, name='staff_profile'),
    path('password/', views.change_password, name='change_password'),
    path('delete/', views.delete_account, name='delete_account'),

]
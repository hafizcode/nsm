from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/staff/add/', views.add_staff, name='add_staff'),
    path('admin/staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('admin/staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),

    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
    path('staff/upload/', views.upload_file, name='upload_file'),
    path('manage-files/', views.manage_files, name='manage_files'),
    path('files/edit/<int:file_id>/', views.edit_file, name='edit_file'),
    path('files/delete/<int:file_id>/', views.delete_file, name='delete_file'),
    path('staff/profile/', views.staff_profile, name='staff_profile'),

    path('categories/', views.category_list, name='category_list'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category, name='edit_category'),
    path('categories/delete/<int:category_id>/', views.delete_category, name='delete_category'),

    path('download/<int:file_id>/', views.download_file, name='download_file'),

    path('groups/add/', views.add_group, name='add_group'),
    path('groups/edit/<int:group_id>/', views.edit_group, name='edit_group'),
    path('groups/delete/<int:group_id>/', views.delete_group, name='delete_group'),
]

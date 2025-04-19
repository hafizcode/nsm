from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, UploadedFile, Category, SubjectGroup
from django.contrib.auth.decorators import user_passes_test
from .forms import GroupForm
from .forms import StaffCreationForm, UploadFileForm, CategoryForm, EditStaffForm
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404
from django.contrib import messages
import os

# Admin Login

def is_admin(user):
    return user.is_superuser

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.is_superuser:
                return redirect('admin_dashboard')  # ✅ URL name
            elif user.is_staff:
                return redirect('staff_dashboard')  # ✅ URL name
            else:
                return redirect('login')  # or handle unauthorized access
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

# Admin: Manage Staff

@user_passes_test(is_admin)
def admin_dashboard(request):
    staff_members = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'admin/dashboard.html', {'staff_members': staff_members})

@user_passes_test(is_admin)
def add_staff(request):
    if request.method == 'POST':
        form = StaffCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.save()
            Profile.objects.create(
                user=user,
                full_name=form.cleaned_data['full_name'],
                phone=form.cleaned_data['phone'],
                department=form.cleaned_data['department'],
                profile_image=form.cleaned_data['profile_image']
            )
            return redirect('admin_dashboard')
    else:
        form = StaffCreationForm()
    return render(request, 'admin/add_staff.html', {'form': form})

@user_passes_test(is_admin)
def edit_staff(request, staff_id):
    user = get_object_or_404(User, id=staff_id)
    profile = user.profile
    form = EditStaffForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    return render(request, 'admin/edit_staff.html', {'form': form})

@user_passes_test(is_admin)
def delete_staff(request, staff_id):
    user = get_object_or_404(User, id=staff_id)
    user.delete()
    return redirect('admin_dashboard')

def admin_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

def group_list(request):
    groups = SubjectGroup.objects.all()
    return render(request, 'pages/group_list.html', {'groups': groups})

@admin_required
def add_group(request):
    if request.method == 'POST':
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'admin/groups/add_group.html', {'form': form})

@admin_required
def edit_group(request, group_id):
    group = get_object_or_404(SubjectGroup, id=group_id)
    if request.method == 'POST':
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'admin/groups/edit_group.html', {'form': form, 'group': group})

@admin_required
def delete_group(request, group_id):
    group = get_object_or_404(SubjectGroup, id=group_id)
    group.delete()
    return redirect('group_list')


# Staff File Management

@login_required
def staff_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'staff/staff_profile.html', {'profile': profile})

@login_required
def staff_dashboard(request):
    files = UploadedFile.objects.filter(uploaded_by=request.user)
    recent_file = UploadedFile.objects.filter(uploaded_by=request.user).order_by('-uploaded_at').first()
    file_count = files.count()
    return render(request, 'staff/dashboard.html', {
        'files': files, 'file_count': file_count, 'recent_file': recent_file
    })

@login_required
def upload_file(request):
    form = UploadFileForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        uploaded_file = form.save(commit=False)
        uploaded_file.uploaded_by = request.user
        uploaded_file.save()
        return redirect('staff_dashboard')
    return render(request, 'staff/upload_file.html', {'form': form})

@login_required
def manage_files(request):
    files = UploadedFile.objects.filter(uploaded_by=request.user)
    return render(request, 'staff/manage_files.html', {'files': files})

@login_required
def edit_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id, uploaded_by=request.user)

    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES, instance=uploaded_file)
        if form.is_valid():
            form.save()
            return redirect('manage_files')
    else:
        form = UploadFileForm(instance=uploaded_file)

    return render(request, 'staff/edit_file.html', {'form': form})

@login_required
def delete_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id, uploaded_by=request.user)

    if request.method == 'POST':
        uploaded_file.delete()
        return redirect('manage_files')

    return render(request, 'staff/delete_file.html', {'file': uploaded_file})


# List all categories
@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'staff/category_list.html', {'categories': categories})

# Add a new category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'staff/add_category.html', {'form': form})

# Edit a category
@login_required
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'staff/edit_category.html', {'form': form})

# Delete a category
@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'staff/delete_category.html', {'category': category})

def download_file(request, file_id):
    uploaded_file = get_object_or_404(UploadedFile, id=file_id)
    uploaded_file.download_count += 1
    uploaded_file.save()

    file_path = uploaded_file.file.path
    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    else:
        raise Http404("File not found.")

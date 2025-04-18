from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from .models import Profile, UploadedFile, Category
from .forms import StaffCreationForm, UploadFileForm, CategoryForm, EditStaffForm

# Admin Login

def is_admin(user):
    return user.is_superuser

def login_view(request):
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            return redirect('staff_dashboard')
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

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

# Staff File Management

@login_required
def staff_profile(request):
    profile = get_object_or_404(Profile, user=request.user)
    return render(request, 'staff/staff_profile.html', {'profile': profile})

@login_required
def staff_dashboard(request):
    files = UploadedFile.objects.filter(uploaded_by=request.user)
    file_count = files.count()
    download_count = sum(file.file.size for file in files)  # replace with actual download tracking
    return render(request, 'staff/dashboard.html', {
        'files': files, 'file_count': file_count, 'download_count': download_count
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

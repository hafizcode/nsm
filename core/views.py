from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UploadFileForm, CategoryForm, StaffRegisterForm, StaffProfileForm
from .models import UploadedFile, Category
from django.db.models import Q
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

# Check if user is staff
def is_staff(user):
    return user.is_staff

def staff_required(user):
    return user.is_authenticated and user.is_staff

# Home Page (open to all)
def home(request):
    return render(request, 'home.html')

def staff_register(request):
    if request.method == 'POST':
        form = StaffRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = True
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('full_name')  # Saving full_name to first_name
            user.save()
            login(request, user)
            return redirect('dashboard')  # or wherever
    else:
        form = StaffRegisterForm()
    return render(request, 'staff_register.html', {'form': form})


# Login View (staff only)
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials or not a staff member.')
    return render(request, 'login.html')

@login_required
def staff_profile(request):
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('staff_profile')
    else:
        form = StaffProfileForm(instance=request.user)
    return render(request, 'staff_profile.html', {'form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps user logged in
            messages.success(request, 'Your password was successfully updated!')
            return redirect('staff_profile')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})

@login_required
def delete_account(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, "Your account has been deleted.")
        return redirect('home')  # or login page

# Logout
def logout_view(request):
    logout(request)
    return redirect('home')

# Dashboard (only logged-in staff)
@login_required
@user_passes_test(is_staff)
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
@user_passes_test(is_staff)
def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = form.save(commit=False)
            uploaded_file.uploaded_by = request.user
            uploaded_file.save()
            return redirect('file_list')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})

@login_required
@user_passes_test(is_staff)
def file_list(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    files = UploadedFile.objects.all()

    if query:
        files = files.filter(Q(title__icontains=query) | Q(label__icontains=query))
    if category_id:
        files = files.filter(category_id=category_id)

    categories = Category.objects.all()

    return render(request, 'file_list.html', {'files': files, 'categories': categories})

@login_required
@user_passes_test(staff_required)
def edit_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    form = UploadFileForm(request.POST or None, request.FILES or None, instance=file)
    if form.is_valid():
        form.save()
        return redirect('file_list')
    return render(request, 'edit_file.html', {'form': form, 'file': file})

@login_required
@user_passes_test(staff_required)
def delete_file(request, file_id):
    file = get_object_or_404(UploadedFile, id=file_id)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return render(request, 'delete_file.html', {'file': file})

@login_required
@user_passes_test(staff_required)
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

@login_required
@user_passes_test(staff_required)
def add_category(request):
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'category_form.html', {'form': form, 'title': 'Add Category'})

@login_required
@user_passes_test(staff_required)
def edit_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    form = CategoryForm(request.POST or None, instance=category)
    if form.is_valid():
        form.save()
        return redirect('category_list')
    return render(request, 'category_form.html', {'form': form, 'title': 'Edit Category'})

@login_required
@user_passes_test(staff_required)
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'category_confirm_delete.html', {'category': category})
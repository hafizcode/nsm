from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UploadFileForm
from .models import UploadedFile, Category
from django.db.models import Q
from .forms import CategoryForm


# Check if user is staff
def is_staff(user):
    return user.is_staff


def staff_required(user):
    return user.is_authenticated and user.is_staff


# Home Page (open to all)
def home(request):
    return render(request, 'home.html')


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


# Logout
def logout_view(request):
    logout(request)
    return redirect('home')


# Register Staff (only staff can access)
@user_passes_test(is_staff)
def register_staff(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
        else:
            User.objects.create_user(username=username, password=password, is_staff=True)
            messages.success(request, 'New staff user created.')
    return render(request, 'register.html')


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


def staff_required(user):
    return user.is_authenticated and user.is_staff


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
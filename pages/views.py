from django.shortcuts import render
from core.models import UploadedFile, Category
from django.db.models import Q


def home(request):
    return render(request, 'home.html')

def public_files(request):
    query = request.GET.get('q')
    category_id = request.GET.get('category')

    files = UploadedFile.objects.all()
    categories = Category.objects.all()

    if query:
        files = files.filter(Q(title__icontains=query) | Q(label__icontains=query))
    if category_id:
        files = files.filter(category_id=category_id)

    return render(request, 'public_files.html', {
        'files': files,
        'categories': categories,
        'selected_category': category_id  # ✅ add this for template
    })

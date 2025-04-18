from django.shortcuts import render
from core.models import UploadedFile, Category
from django.db.models import Q

def public_resources(request):
    query = request.GET.get('q')
    files = UploadedFile.objects.all()
    if query:
        files = files.filter(
            Q(title__icontains=query) |
            Q(label__icontains=query) |
            Q(category__name__icontains=query)
        )
    return render(request, 'pages/resources.html', {'files': files})

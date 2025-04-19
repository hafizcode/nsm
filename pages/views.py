from django.shortcuts import render, get_object_or_404
from core.models import UploadedFile, Category, SubjectGroup
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

def home_view(request):
    return render(request, 'home.html')

def group_list_view(request):
    groups = SubjectGroup.objects.all()  # Correctly reference the model
    return render(request, 'pages/group_list.html', {'groups': groups})

def group_detail_view(request, group_id):
    group = get_object_or_404(SubjectGroup, id=group_id)  # Use 'group' as the instance name
    query = request.GET.get('q', '')
    files = UploadedFile.objects.filter(group=group)  # Corrected filter by group

    if query:
        files = files.filter(title__icontains=query) | files.filter(label__icontains=query)

    return render(request, 'pages/group_detail.html', {
        'group': group,  # Use the variable name 'group' here
        'files': files,
        'query': query
    })

from django import forms
from .models import UploadedFile
from .models import Category


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'label', 'file', 'category']  # ✅ Add category field


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

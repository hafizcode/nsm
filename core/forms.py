from django import forms
from .models import UploadedFile, Category, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UploadedFile, Category, Profile, SubjectGroup

class GroupForm(forms.ModelForm):
    class Meta:
        model = SubjectGroup
        fields = ['name']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'label', 'file', 'category', 'group']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

class StaffCreationForm(UserCreationForm):
    full_name = forms.CharField()
    phone = forms.CharField()
    department = forms.CharField()
    email = forms.EmailField()
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class EditStaffForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['full_name', 'phone', 'department', 'profile_image']

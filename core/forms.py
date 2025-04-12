from django import forms
from .models import UploadedFile, Category, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class StaffRegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100, required=True)
    phone = forms.CharField(max_length=15, required=False)
    department = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'full_name', 'phone', 'department', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.is_staff = True  # Mark user as staff
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                profile_image=self.cleaned_data.get('profile_image') or 'profile_pics/default.png'
            )
        return user


class StaffProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['title', 'label', 'file', 'category']  # ✅ Add category field


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']

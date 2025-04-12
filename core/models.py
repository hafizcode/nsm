from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class UploadedFile(models.Model):
    title = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)  # ✅ New field

def default_profile_image():
    return 'profile_pics/default.png'  # This should be inside your static/media folder

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='profile_pics/', default=default_profile_image)

    def __str__(self):
        return f"{self.user.username}'s Profile"

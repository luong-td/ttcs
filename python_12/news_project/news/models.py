from django.db import models
from django.db.models.deletion import CASCADE
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.conf import settings

# Create your models here.

class Category (models.Model):
    title = models.CharField(max_length=400)
    image = models.ImageField(upload_to="imgs/", blank=True)

    def __str__(self):
        return self.title

class New (models.Model):
    title = models.CharField(max_length=400)
    image = models.ImageField(upload_to="imgs/", blank=True)
    detail_view = models.CharField(max_length=500, blank=True, null=True)
    detail = RichTextUploadingField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    
class Feedback(models.Model):
    message = models.CharField(max_length=2000)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    subject = models.CharField(max_length=200)

    def __str__(self):
        return self.subject
class Comment(models.Model):
    new = models.ForeignKey(New, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateField(auto_now_add=True)


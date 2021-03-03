from django.db import models

# Create your models here.
class Photo(models.Model):
    created_at = models.DateTimeField(auto_now_add=True) 
    title = models.CharField(max_length=100)
    photo = models.FileField(upload_to='resumes')
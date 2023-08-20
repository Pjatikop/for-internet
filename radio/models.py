from django.db import models
from django.contrib.auth.models import User


class Radio(models.Model):
    title = models.CharField(max_length=200)
    featured_image = models.ImageField(upload_to='projects/radioimages', default='default.jpg')
    demo_link = models.CharField(max_length=200, null=True, blank=True)
    name_link = models.CharField(max_length=200, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

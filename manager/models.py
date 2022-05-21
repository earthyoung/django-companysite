from django.db import models

from website.settings import MEDIA_ROOT

# Create your models here.

class CompanyImg(models.Model):
    id = models.AutoField(primary_key=True)
    img = models.ImageField(upload_to="imageboard/images", blank=True, default=None)


class Company(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=13)
    business_name = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True, null=True)
    img1 = models.ForeignKey(CompanyImg, on_delete=models.SET_NULL, null=True, related_name='company1')
    img2 = models.ForeignKey(CompanyImg, on_delete=models.SET_NULL, null=True, related_name='company2')




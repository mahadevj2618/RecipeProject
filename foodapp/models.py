from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Photo(models.Model):
    name=models.CharField(max_length=122)
    desc=models.CharField(max_length=122)
    img=models.FileField(max_length=122)

class Item(models.Model):
    def __str__(self):
        return self.item_name
    item_name=models.CharField(max_length=122)
    item_desc=models.CharField(max_length=122)
    item_price=models.IntegerField()
    item_image=models.FileField(max_length=122)

class About(models.Model):
    title=models.CharField(max_length=122)
    descript=models.CharField(max_length=200)


class Profile(models.Model):
    user_instance=models.OneToOneField(User,on_delete=models.CASCADE)
    image=models.FileField(max_length=122)
    bio = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    education=models.TextField(max_length=122)
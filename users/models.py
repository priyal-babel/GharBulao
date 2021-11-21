from django.db import models
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
cities = [
    ('delhi','Delhi'),
    ('mumbai','Mumbai'),
    ('kolkata','Kolkāta'),
    ('bangalore','Bangalore'),
    ('chennai','Chennai'),
    ('pune','Pune'),
    ('ahmedabad','Ahmedabad'),
    ('patna','Patna'),
    ('hyderabad','Hyderabad'),
    ('bhuj','Bhuj'),
    ('vadodara','Vadodara'),
    ('dehradun','Dehradun'),
    ]

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_Picture = models.ImageField(default='default.png',upload_to='profile_pics')
    gender = models.CharField(max_length=10)
    mobile_No = models.CharField(max_length=10)
    city = models.CharField(max_length=50, choices=cities, default='Mumbai')
    birth_Date = models.DateField()   

    REQUIRED_FIELDS = ['profile_Picture','gender','mobile_No','city','birth_Date']

    def __str__(self):
        return {self.user.username}

    def save(self):
        super().save()
        img = Image.open(self.profile_pic.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_pice.path)



    
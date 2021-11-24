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

states = [
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
    profile_picture = models.ImageField(default='default.png',upload_to='profile_pics')
    gender = models.CharField(max_length=10)
    mobile_no = models.CharField(max_length=10)
    bio = models.CharField(max_length=1000)
    city = models.CharField(max_length=50, choices=cities, default='Mumbai')
    birth_date = models.DateField(null=True)   

    REQUIRED_FIELDS = ['profile_picture','gender','mobile_no','city','birth_date']

    def __str__(self):
        return str(self.user.username)

    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        img = Image.open(self.profile_picture.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.profile_picture.path)

class Post(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE) 
    address = models.TextField()
    pincode = models.IntegerField(null=True)
    city = models.CharField(max_length=50, choices=cities, default='Mumbai')
    state =  models.CharField(max_length=50, choices=states, default='Maharashtra')
    Area = models.DecimalField(max_digits=6,default=0.0,decimal_places=2)
    amenities = models.CharField(max_length=500,default='[]')
    timestamp = models.DateTimeField(auto_now=True)
       
    def __str__(self):
        return str(self.user.username)

class Image(models.Model):
    post = models.ForeignKey(Post, default=None,on_delete=models.CASCADE)
    image = models.ImageField(upload_to='property_pics',
                              verbose_name='Image')
    def __str__(self):
        return str(self.post)
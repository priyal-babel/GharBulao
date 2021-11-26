from django.contrib import admin
from .models import Profile,Post,Image,Reviews

# Register your models here.
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Image)
admin.site.register(Reviews)
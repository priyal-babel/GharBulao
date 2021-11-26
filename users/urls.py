from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('',views.home,name='home'),
    path('profile/',views.profileUpdate,name='profile'),
    path('post/',views.posts,name='post'),
    path('post/review',views.review,name='review'),
    #  path('data/',views.getdata,name='data'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name="logout"),
]
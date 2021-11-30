from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('register/',views.register,name='register'),
    path('',views.home,name='home'),
    path('about/',views.about,name='about'),
    path('contact/',views.contact,name='contact'),
    path('profile/',views.profileUpdate,name='profile'),
    path('post/',views.posts,name='post'),
    path('postList/',views.postList,name='postList'),
    path('showPost/<int:pk>',views.showPost,name='showPost'),
    #  path('data/',views.getdata,name='data'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name="logout"),
]



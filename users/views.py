from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.
def register(request):
   if(request.method == 'POST'):
      u_form = UserRegisterForm(request.POST)
      # p_form = ProfileUpdateForm(request.POST,request.FILES or None)
      if u_form.is_valid():
         u_form.save()
         # p_form.save()
         username = u_form.cleaned_data.get('username')
         print("username : " , username)
         messages.success(request,f"Username {username}, your account is created successfully. Login to use the available features..")
         return redirect('login')
   else:
      # this is the default form that django gives us with all basic fileds required for the user to register along with the validation stuff
      u_form = UserRegisterForm()
      # p_form = ProfileUpdateForm()
   return render(request,'users/register.html',{'u_form' : u_form})


def home(request):
   return render(request,'users/home.html')
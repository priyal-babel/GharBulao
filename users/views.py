from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Image, Post, Reviews

from users.models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm,PostForm

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
      u_form = UserRegisterForm()
   return render(request,'users/register.html',{'u_form' : u_form})

@login_required
def profileUpdate(request):
   profile = Profile.objects.get(user=request.user)
   if request.method == 'POST':
      u_form = UserUpdateForm(request.POST,instance=request.user)
      p_form = ProfileUpdateForm(request.POST,request.FILES,instance=profile)
      if u_form.is_valid() and p_form.is_valid():
         u_form.save()
         p_form.save()
         messages.success(request, f'Your profile has been updated.')
         return redirect('profile')
   else:
      u_form = UserUpdateForm(instance=request.user)
      p_form = ProfileUpdateForm(instance=profile)
      context = {
			'u_form': u_form,
         'p_form': p_form,
		}
      return render(request, 'users/profile.html',context)

def home(request):
   return render(request,'users/home.html')

@login_required
def posts(request):
   
   if request.method == 'POST':
      pform = PostForm(request.POST)
      images = request.FILES.getlist('image')

      if pform.is_valid():
         pst = pform.save(commit=False)
         pst.user = request.user
         pst.save()
         print("POSTTTTTTTTTTTTT",pst.post_id)
         for img in images:
            Image.objects.create(post=pst, image=img)
         
         messages.success(request, f'Your post has been updated.')
         return redirect('post')
   else:
      form = PostForm()
      context = {
			'form': form,
		}
   return render(request,'users/post.html',context)


@login_required
def review(request):
   if request.POST.get('action') == '':
      review = request.POST.get('review')
      rating = request.POST.get('rating')
      post = Post.objects.get(id=11)
      print("REVIEWWWWWWWWW",review)
      print("DATAAA",rating)
      # Reviews.objects.create(
      #    review = review,
      #    rating = rating,
      #    user = request.user,
      #    post = post,
      #    )
      print("HELLOOOOOOO")
      return HttpResponse('<html></html>')
   return render(request,'users/reviews.html')

def showPost(request,pk):
   return render(request,'users/showPost.html')

def postList(request):
   return render(request,'users/postList.html')

# def getdata(request):
#    p = Post.objects.all()
#    print(p[0].id, p[0].city, p[0].address)
#    html = f"<html><body>Data: {p[0].id}</body></html>"
#    return HttpResponse(html)
   
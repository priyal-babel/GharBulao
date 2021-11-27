from django.contrib.auth import login
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Img, Post, Reviews
from django.db.models import Avg

from users.models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm,PostForm, searchForm

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
         for img in images:
            Img.objects.create(post=pst, image=img)
         
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
      post = Post.objects.get(id=11)  #TODO
      Reviews.objects.create(
         review = review,
         rating = rating,
         user = request.user,
         post = post,
         )
      return HttpResponse('<html></html>')
   return render(request,'users/reviews.html')


@login_required
def showPost(request,pk):
   return render(request,'users/showPost.html')

@login_required
def postList(request):

   form = searchForm()
   if request.method == 'POST':
      form = searchForm(request.POST)
      if form.is_valid():
         # post = Post.objects.filter(city__contains=form.cleaned_data.get('search'))
         posts = Img.objects.filter(post__city__contains = form.cleaned_data.get('search'))
   else:
      posts = Img.objects.all()
      review_post = Post.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('avg_rating')
      print("LALALALLA",review_post)
      # for post in review_post:
      #    rating = Reviews.objects.filter(post=post)


   return render(request,'users/postList.html',{'posts' : posts, 'form': form})

# def getdata(request):
#    p = Post.objects.all()
#    print(p[0].id, p[0].city, p[0].address)
#    html = f"<html><body>Data: {p[0].id}</body></html>"
#    return HttpResponse(html)
   
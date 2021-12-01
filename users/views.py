from django.contrib.auth import login
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Img, Post, Reviews
from django.db.models import Avg
from django.contrib.auth.decorators import user_passes_test

from users.models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm,PostForm, searchForm

def user_is_not_logged_in(user):
   return not user.is_authenticated()

@user_passes_test(user_is_not_logged_in, login_url='/')
def register(request):
 if not request.user:
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
 else:
      return redirect('home')

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
def showPost(request,pk):
   post = Post.objects.get(id=pk) 
   if request.POST.get('action') == '':
      review = request.POST.get('review')
      rating = request.POST.get('rating')
      reviews  = Reviews.objects.filter(user=request.user,post=post)
      if reviews:
         return HttpResponseNotFound('error message')
      else:
         Reviews.objects.create(
            review = review,
            rating = rating,
            user = request.user,
            post = post,
            )
         return HttpResponse('<html></html>')
   return render(request,'users/showPost.html',context={'post':post})

@login_required
def postList(request):
   r_post = Post.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]
   review_post = []
   for r in r_post:
      x = [Img.objects.select_related().filter(post=r)]
      x.append(r.avg_rating)
      review_post.append(x)
   form = searchForm()
   if request.method == 'POST':
      form = searchForm(request.POST)
      if form.is_valid():
         # post = Post.objects.filter(city__contains=form.cleaned_data.get('search'))
         if not form.cleaned_data.get('search') == 'None':
           p = Img.objects.filter(post__city__contains = form.cleaned_data.get('search'))
         else:
           p = Img.objects.all()
   else:
      p = Img.objects.all().order_by('-post__timestamp')

   posts = {}
   for post in p:
      if post.post.id not in posts:
         posts[post.post.id] = []
      posts[post.post.id].append(post)

   return render(request,'users/postList.html',{'posts' : posts, 'form': form, 'reviews':review_post})


def about(request):
   return render(request,'users/about.html')

def contact(request):
   try:
      # if request.POST.get('action') == 'contact':
      # if request.is_ajax():
      if request.method == 'POST':
         full_name = request.POST.get('full_name')
         email = request.POST.get('email')
         education  = request.POST.get('education')
         message  = request.POST.get('message')
         print("FN : " + full_name + " email : " + email + " education : " + education + " message : " + message)
         return HttpResponse('<html></html>')
   except:
      return HttpResponseNotFound('<html></html>')
   return render(request,'users/contact.html')

# def getdata(request):
#    p = Post.objects.all()
#    print(p[0].id, p[0].city, p[0].address)
#    html = f"<html><body>Data: {p[0].id}</body></html>"
#    return HttpResponse(html)
   
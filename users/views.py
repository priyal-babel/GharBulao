from django.contrib.auth import login
from django.http.response import HttpResponse, HttpResponseNotFound
from django.shortcuts import redirect, render
# from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Img, Post, Reviews
from django.db.models import Avg
from ast import literal_eval
from datetime import date
from users.models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm, UserUpdateForm,PostForm, searchForm

def register(request):
   if request.user!="AnonymousUser":
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
   services = [{"img" : "https://slowviking.com/wp-content/uploads/2017/08/Levers-Couchsurfing.jpg","title" : "Book Your Dream House"},{"img" : "https://hips.hearstapps.com/hmg-prod.s3.amazonaws.com/images/hotel-booking-apps-1533324348.jpg","title" : "Post Yur Own Property"},{"img" : "https://www.thebrokebackpacker.com/wp-content/uploads/2016/07/CS.jpg","title":"Make New Memories"}]
   return render(request,'users/home.html',{'services':services})

@login_required
def posts(request):
   
   if request.method == 'POST':
      pform = PostForm(request.POST)
      p = Post.objects.filter(user=request.user)
      if p:
          messages.warning(request, f'You have already posted your property.')
          return redirect('post')
      else:   
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
   info = {}
   info['post'] = Post.objects.get(id=pk) 
   info['images'] = Img.objects.filter(post=info['post']).defer('post')
   info['reviews'] = Reviews.objects.filter(post=info['post']).defer('post')
   icons = {
      'wifi' : 'fas fa-wifi',
      'TV' : 'fas fa-tv',
      'music system' : 'fas fa-music',
      'AC' : 'fas fa-wind',
      'swimming pool' : 'fas fa-swimming-pool',
      'gym' : 'fas fa-dumbbell',
      'indoor sports' : 'fas fa-volleyball-ball'
   }

   if request.POST.get('action') == '':
      review = request.POST.get('review')
      rating = request.POST.get('rating')
      reviews  = Reviews.objects.filter(user=request.user,post=info['post'] )
      if reviews:
         return HttpResponseNotFound('error message')
      else:
         Reviews.objects.create(
            review = review,
            rating = rating,
            user = request.user,
            post = info['post'],
            )
         return HttpResponse('<html></html>')
   info['post'].amenities = literal_eval(info['post'].amenities)
   # print( info['post'].amenities , "     " , type(info['post'].amenities))
   return render(request,'users/showPost.html', context={'info':info,'icons':icons})

@login_required
def postList(request):
   r_post = Post.objects.annotate(avg_rating=Avg('reviews__rating')).order_by('-avg_rating')[:4]
   review_post = []
   for r in r_post:
      x = [Img.objects.select_related().filter(post=r)]
      if r.avg_rating:
         r.avg_rating = round(r.avg_rating,1)
      else:
         r.avg_rating = 0
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

@login_required
def receipt(request, pk):
   post = Post.objects.get(id=pk)
   img = Img.objects.filter(post=post)
   post.date = date.today()
   post.img = img[0].image
   return render(request,'users/receipt.html',context={'post':post})

# def getdata(request):
#    p = Post.objects.all()
#    print(p[0].id, p[0].city, p[0].address)
#    html = f"<html><body>Data: {p[0].id}</body></html>"
#    return HttpResponse(html)
   
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.utils.regex_helper import Choice
from .models import Profile

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
    
gender_choice = [
    ('male','Male'),
    ('female','Female'),
    ('other','Other')
]

class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2']

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class ProfileUpdateForm(forms.ModelForm):
    profile_Picture = forms.ImageField()
    gender = forms.CharField(max_length=10, widget=forms.Select(choices=gender_choice))
    mobile_No = forms.CharField(max_length=10)
    city = forms.CharField(widget=forms.Select(choices=cities))
    birth_Date = forms.DateField(
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
    )
)
    class Meta:
        model = Profile
        fields = ['gender','mobile_No','city','birth_Date','profile_Picture']
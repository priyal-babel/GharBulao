from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import widgets
from django.utils.regex_helper import Choice
from .models import Profile
from django.db import transaction

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
    # first_name 
    gender = forms.CharField(max_length=10, widget=forms.Select(choices=gender_choice))
    mobile_no = forms.CharField(max_length=10,label="Mobile No.")
    city = forms.CharField(widget=forms.Select(choices=cities))
    birth_date = forms.DateField(
    label="Birth Date",
    widget=forms.TextInput(     
        attrs={
        'type': 'date',
        }
    )
)

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email','password1','password2','gender','mobile_no','city','birth_date']
        widgets = {
          'first_name': forms.TextInput(attrs={'class': 'input'}),
          'last_name': forms.TextInput(attrs={'class': 'input'}),
          'email': forms.EmailInput(attrs={'class': 'input'}),
          'gender': forms.TextInput(attrs={'class': 'input'}),
            'mobile_no': forms.TextInput(attrs={'class': 'input'}),
            'city': forms.TextInput(attrs={'class': 'input'}),
            'birth_date': forms.DateInput(attrs={'class': 'input'}) ,
        }
        
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.password1 = self.cleaned_data.get('password1')
        user.password2 = self.cleaned_data.get('password2')
        user.save()
        profile = Profile.objects.create(user=user)
        profile.gender = self.cleaned_data.get('gender')
        profile.mobile_no = self.cleaned_data.get('mobile_no')
        profile.birth_date = self.cleaned_data.get('birth_date')
        profile.city = self.cleaned_data.get('city')
        profile.save()
        return user

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name','last_name','username','email']

class ProfileUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False,label="Profile Picture")
    gender = forms.CharField(max_length=10, widget=forms.Select(choices=gender_choice))
    mobile_no = forms.CharField(max_length=10,label="Mobile No.")
    city = forms.CharField(widget=forms.Select(choices=cities))
    birth_date = forms.DateField(
    label="Birth Date",
    widget=forms.TextInput(     
        attrs={'type': 'date'} 
    )
)
    class Meta:
        model = Profile
        fields = ['gender','mobile_no','city','birth_date']
        widgets = {
          'gender': forms.TextInput(attrs={'class': 'input'}),
          'mobile_no': forms.TextInput(attrs={'class': 'input'}),
          'city': forms.TextInput(attrs={'class': 'input'}),
          'birth_date': forms.DateInput(attrs={'class': 'input'}),
        }
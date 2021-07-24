from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from .models import NeighborHood,Business,Post

class SignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=100, help_text='Last Name')
  last_name = forms.CharField(max_length=100, help_text='Last Name')
  email = forms.EmailField(max_length=150, help_text='Email')

  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

class CreateNeighborHoodForm(forms.ModelForm):
  class Meta:
    model = NeighborHood
    fields = ('name','location','description','population','police_count','hospital_count','image')

class CreateBusinessForm(forms.ModelForm):
  class Meta:
    model = Business
    fields = ('name','description','email')

class CreatePostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ('title','post')

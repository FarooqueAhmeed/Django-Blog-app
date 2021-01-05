from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from blog.models import Blog



class BlogForm(ModelForm):
    class Meta:
        model = Blog
        fields = ['category','title','content']


class Blog_update_Form(ModelForm):
    class Meta:
        model = Blog
        fields = ['title','content']




class SignUpForm(UserCreationForm):
    useremail = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ['username','useremail', 'password1', 'password2']
from django import forms
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
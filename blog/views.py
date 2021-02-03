import io
import os
import sys

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.uploadedfile import InMemoryUploadedFile

from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.migrations import serializer
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.urls import reverse
from .forms import BlogForm, Blog_update_Form, BlogImageForm, UserProfileForm
from .models import Blog, Comments, Favorite, Following, UserProfile




def user_signup(request):
    if request.user.is_authenticated:
        return render(request, 'home.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        useremail = request.POST.get('useremail')
        password = request.POST.get('password')
        if username_exists(username) == False and usermail_exists(useremail) == False:
            user = User.objects.create_user(username, useremail, password)
            login(request, user)

            return render(request, 'login.html')
        else:
            messages.error(request, 'User Name or email already exist.')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')


def user_login(request):
    if request.user.is_authenticated:
        blogs = Blog.objects.all()
        context = {'blogs': blogs}

        return render(request, 'home.html',context)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                messages.error(request, 'Your account was inactive.')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid login details given.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


'''Called when user logs out'''


def user_logout(request):
    logout(request)
    messages.success(request, 'User signed out successfully')
    return render(request, 'login.html')


def username_exists(username):
    if User.objects.filter(username=username).exists():
        return True
    return False


def usermail_exists(useremail):
    if User.objects.filter(email=useremail).exists():
        return True
    return False


def index(request):
    blogs = Blog.objects.all()



    context= {'blogs':blogs}


    return render(request, 'index.html',context)


#when user will loging this function will be called 1st
@login_required()
def home(request):

    # getting all users blogs
    blogs = Blog.objects.all()
    count_all_blogs = Blog.objects.all().count()
    count_all_users = User.objects.all().count()

    #
    # user_p = UserProfile.objects.all()
    # print(user_p)



    try:
       avatar = UserProfile.objects.get(user=request.user)


       context = {
           'blogs': blogs,
           'count_all_blogs': count_all_blogs,
           'count_all_users': count_all_users,
           'avatar': avatar,
       }

       return render(request, 'home.html', context)

    except UserProfile.DoesNotExist:
           avatar = None
           print(avatar)
    context = {
        'blogs': blogs,
        'count_all_blogs':count_all_blogs,
        'count_all_users':count_all_users,
        'avatar':avatar,
    }

    return render(request, 'home.html',context)




#
#
# def upload_pic(request):
#     if request.method == 'POST':
#         form = ImageUploadForm(request.POST, request.FILES)
#         if form.is_valid():
#             m = ExampleModel.objects.get(pk=id)
#             m.model_pic = form.cleaned_data['image']
#             print(m)
#             m.save()
#             return HttpResponse('image upload success')
#     return HttpResponseForbidden('allowed only via POST')




# this fuction will be called when any user wants view any user profile
@login_required()
def user(request, pk):

    # getting user name
    user = Blog.objects.filter(id=pk)
    user = user.get()
    print(user.user.username)

    #getting the user for retriving all blogs to the user
    get_user = User.objects.get(blog=user)
    print(get_user)

    #getting the exact/logined user which is requesting
    r_user = User.objects.get(username__exact=request.user)
    print(r_user)


    try:
        followers_count = Following.objects.filter(follows=get_user).count()
        print(followers_count)

        check2 = Following.objects.filter(follows=r_user)
        print(check2)

        # check1 is for is to check if the status of the viewed user is true or false(check if exact user followibg or not)
        check1 = Following.objects.filter(follows=get_user).filter(a_user=r_user).filter(boolean=True)
        check1 = check1.get(boolean=True)
        print(check1)

        all_blogs = Blog.objects.filter(user=get_user)
        print(all_blogs)

        blog_count = Blog.objects.filter(user=get_user).count()


        context = {
            'check1': check1 ,
            'get_user':get_user,
            'all_blogs':all_blogs,
            'blog_count':blog_count,
            'followers_count':followers_count,
        }
        return render(request, 'user.html', context)

    except:

        print('not following')

        user = Blog.objects.filter(id=pk)
        user = user.get()


        get_user = User.objects.get(blog=user)
        print(get_user)

        all_blogs = Blog.objects.filter(user=get_user)
        print(all_blogs)

        blog_count = Blog.objects.filter(user=get_user).count()

        followers_count = Following.objects.filter(follows=get_user).count()
        print(followers_count)


        context = {
            'check1': check1,
            'user':user,
            'get_user':get_user,
             'all_blogs':all_blogs,
            'blog_count':blog_count,
            'followers_count': followers_count,
             }
        return render(request, 'user.html', context)




@login_required
def follow_user(request,pk):
    user = User.objects.filter(blog=pk)
    user = user.get()
    follow = Following(follows=user,a_user=request.user)
    follow.boolean = True
    follow.save()
    messages.success(request, f"following")
    return redirect('home')


@login_required
def my_followed(request):
    followed = Following.objects.filter(a_user_id__exact=request.user)
    #my_followers = Following.objects.filter(a_user=id)
    #print(my_followers)

    context = {'followed': followed}

    return render(request, 'my_followed.html', context)


@login_required
def my_followers(request,pk):

    my_followers = Following.objects.filter(follows=pk)
    print(my_followers)
    my_followers_count = Following.objects.filter(follows=pk).count()
    print(my_followers_count)


    if my_followers == None:
        messages.info(request, 'Nobody follows you !')
        return render(request, 'my_followers.html')
    else:
        context = {
            'my_followers': my_followers,
            'my_followers_count':my_followers_count,
        }
        return render(request, 'my_followers.html', context)


@login_required
def unfollow(request, pk):
    boolean_false = Following.objects.get(id=pk)
    boolean_false.delete()

    return redirect('home')






@login_required()
def add_blog(request):
    if request.method == "POST":

        category = request.POST.get('category')
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES['image']

        # image = Image.open(image)
        # image = image.convert('RGB')
        # image = image.resize((800, 800), image.ANTIALIAS)
        # output = io.BytesIO()
        # image.save(output, format='JPEG', quality=85)
        # output.seek(0)
        # return InMemoryUploadedFile(output, 'ImageField',image.name,'image/jpeg',sys.getsizeof(output), None)
        #

        blog = Blog(category=category,title=title,content=content,image=image,user=request.user)
        blog.save()

        return redirect('/home')


    else:
        form = BlogForm()
    return render(request,'add_blog.html',{'form':form})








#
#
# @login_required()
# def a_blog(request):
#     form = BlogForm(request.POST or None, request.FILES or None)
#     if form.is_valid():
#         instance = form.save(commit=False)
#         instance.user = request.user
#         instance.save()
#     return redirect("/home")




@login_required()
def delete_blog(request, pk):
    blog = Blog.objects.get(id=pk)
    blog.delete()
    return redirect("/home")

@login_required()
def edit(request, pk):
    blogs = Blog.objects.get(id=pk)
    context ={'blogs': blogs}
    return render(request,'edit.html',context)


@login_required()
def update(request, pk):
    blogs = Blog.objects.get(id=pk)
    form = Blog_update_Form(request.POST, instance = blogs)
    if form.is_valid():
        form.save()
        return redirect("/home")
    context = {'blogs': blogs}
    return render(request, 'edit.html',context)




def read_more(request, pk):
    blogs = Blog.objects.filter(id=pk)
    blogs = blogs.get()
    comment = Comments.objects.filter(blog=blogs)
    comments_count = Comments.objects.filter(blog=blogs).count()


    blogs = Blog.objects.filter(id=pk)

    return render(request, 'read_more.html', {'comment': comment,'blogs':blogs, 'comments_count':comments_count})



@login_required()
def comment(request, pk):
    if request.method == "POST":
        comment = request.POST['comment']
        blogs = Blog.objects.get(id=pk)
        comment = Comments(user=request.user,blog=blogs,comment=comment)
        comment.save()


        return read_more(request,pk)
    else:
        return home(request)


@login_required
def fav(request, pk):
    blog = Blog.objects.filter(id=pk)
    favorite = Favorite(user=request.user, blog=blog.get())
    blog_title = blog.get().title


    check_for_exist = Favorite.objects.filter(blog_id=pk).exists()
    print(check_for_exist)
    if check_for_exist == True:
        return redirect('favorites')
    else:
        favorite.save()
        messages.success(request, f"{blog_title} Blog added to favorites")
        return redirect('home')


@login_required
def favorites(request):
    fav = Favorite.objects.filter(user__exact=request.user)
    blogs = Blog.objects.all()
    print(fav)

    return render(request, 'favorites.html',  {'fav': fav,'blogs':blogs})




@login_required
def deletefav(request, pk):
    fav = Favorite.objects.filter(id=pk, ).get()
    blog_title = fav.blog.title
    fav.delete()
    messages.success(request, f" {blog_title}  Deleted")
    return redirect('favorites')




@login_required
def my_blogs(request):
    my = Blog.objects.filter(user__exact=request.user)


    return render(request, 'my_blogs.html',  {'my': my})




@login_required
def search_by_blog_title(request):
    search = request.GET['title']
    search = Blog.objects.filter(title__icontains=search)
    print(search)
    if search == []:
        msg = 'Not found'
        return render(request,"search_by_blog_title.html",{'msg':msg})
    else:
        return render(request,'search_by_blog_title.html',  {'search': search})


''' 
@login_required()
def edit_profile(request, pk):
    get_user = User.objects.get(id=pk)
    context ={'get_user': get_user}
    return render(request,'profile.html',context)
 '''
#
# try:
#     avatar = UserProfile.objects.get(user=request.user)
#
#     context = {
#         'blogs': blogs,
#         'count_all_blogs': count_all_blogs,
#         'count_all_users': count_all_users,
#         'avatar': avatar,
#     }
#
#     return render(request, 'home.html', context)
#
# except UserProfile.DoesNotExist:
#     avatar = None
#     print(avatar)
# context = {
#     'blogs': blogs,
#     'count_all_blogs': count_all_blogs,
#     'count_all_users': count_all_users,
#     'avatar': avatar,
# }


@login_required()
def profile(request, pk):
    user = User.objects.filter(id=pk)
    user = user.get()
    form = UserProfileForm (instance=user)


    try:
        avatar = UserProfile.objects.get(user=request.user)

        print(avatar)
        print(user)

        return render(request, 'profile.html', {'user':user,'avatar':avatar,'form':form})

    except UserProfile.DoesNotExist:
        avatar = None
        print(avatar)


    return render(request, 'profile.html', {'user':user,'avatar':avatar,'form':form})




@login_required()
def upload_profile(request):
    # img = UserProfile.objects.get(id=pk)
    # img.delete()
    form = UserProfileForm(request.POST or None, request.FILES)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect("/home")
    return redirect("/home")


@login_required()
def update_profile(request, pk):
    user = User.objects.filter(id=pk)
    user = user.get()
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')

        get_user = User(username=username,email=email)
        get_user.save()
        return redirect("/home")
    context = {'user': user}
    return render(request, 'profile.html',context)




@login_required()
def remove_img(request,pk):
    img = UserProfile.objects.get(id=pk)
    img.delete()

    return redirect("/home")


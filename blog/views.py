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
from .forms import BlogForm, Blog_update_Form, BlogImageForm, UserProfileForm, UpdateUserForm
from .models import Blog, Comments, Favorite, Following, UserProfile, BIO


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

    # paginations
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    count_all_blogs = Blog.objects.all().count()
    count_all_users = User.objects.all().count()

    recent_blogs = Blog.objects.all().order_by('-created')[:5]
    print(recent_blogs)

    context= {
        'blogs':page_obj,
        'count_all_blogs': count_all_blogs,
        'count_all_users': count_all_users,
        'recent_blogs': recent_blogs,
    }


    return render(request, 'index.html',context)


#when user will loging this function will be called 1st
@login_required()
def home(request):

    # getting all users blogs
    blogs = Blog.objects.all()

    #paginations
    paginator = Paginator(blogs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)


    count_all_blogs = Blog.objects.all().count()
    count_all_users = User.objects.all().count()

    recent_blogs = Blog.objects.all().order_by('-created')[:5]
    print(recent_blogs)



    try:
       avatar = UserProfile.objects.get(user=request.user)


       context = {
           'blogs': page_obj,
           'count_all_blogs': count_all_blogs,
           'count_all_users': count_all_users,
           'avatar': avatar,
           'recent_blogs':recent_blogs,
       }

       return render(request, 'home.html', context)

    except UserProfile.DoesNotExist:
           avatar = None
           print(avatar)
    context = {
        'blogs': page_obj,
        'count_all_blogs':count_all_blogs,
        'count_all_users':count_all_users,
        'avatar':avatar,
        'recent_blogs':recent_blogs,
    }

    return render(request, 'home.html',context)





# this function will be called when any user wants view any user profile
@login_required()
def user(request, pk):
    blog_user_avatar = None
    check1 = False


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
        # get viewed user profile picture
        blog_user_avatar = UserProfile.objects.get(user=get_user)
        print(blog_user_avatar)

        followers_count = Following.objects.filter(follows=get_user).count()
        print(followers_count)

        check2 = Following.objects.filter(follows=r_user)
        print(check2)

        # check1 is for to check if the status of the viewed user is true or false(check if exact user followibg or not)
        check1 = Following.objects.filter(follows=get_user).filter(a_user=r_user).filter(boolean=True)
        check1 = check1.get(boolean=True)
        print(check1)

        all_blogs = Blog.objects.filter(user=get_user)
        print(all_blogs)

        blog_count = Blog.objects.filter(user=get_user).count()





        if blog_user_avatar == None:
            blog_user_avatar = None

            context = {
                'check1': check1,
                'get_user': get_user,
                'all_blogs': all_blogs,
                'blog_count': blog_count,
                'followers_count': followers_count,
                'blog_user_avatar': blog_user_avatar,
                'r_user':r_user,
            }
            return render(request, 'user.html', context)


        else:

            context = {
                'check1': check1,
                'get_user': get_user,
                'all_blogs': all_blogs,
                'blog_count': blog_count,
                'followers_count': followers_count,
                'blog_user_avatar': blog_user_avatar,
                'r_user': r_user,
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
                'blog_user_avatar': blog_user_avatar,
                  'r_user': r_user,
                 }
        return render(request,'user.html',context)
    # finally:
    #
    #
    #        return render(request, 'user.html',context)




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


        blog = Blog(category=category,title=title,content=content,image=image,user=request.user)
        blog.save()

        return redirect('/home')


    else:
        form = BlogForm()
    return render(request,'add_blog.html',{'form':form})










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



@login_required
def read_more(request, pk):
    blogs = Blog.objects.filter(id=pk)
    blogs = blogs.get()

    comment = Comments.objects.filter(blog=blogs)
    comments_count = Comments.objects.filter(blog=blogs).count()

    blogs = Blog.objects.filter(id=pk)

    check_favorited = None
    try:
        check_favorited = Favorite.objects.get(blog_id__in=blogs)
        print(check_favorited)
        return render(request, 'read_more.html', {'comment': comment, 'blogs': blogs, 'comments_count': comments_count,
                                                  'check_favorited': check_favorited, })
    except:

        return render(request, 'read_more.html', {'comment': comment,'blogs':blogs, 'comments_count':comments_count,'check_favorited':check_favorited,})



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


    return render(request, 'favorites.html',  {'fav': fav,})




@login_required
def deletefav(request, pk):
    fav = Favorite.objects.filter(id=pk, ).get()
    blog_title = fav.blog.title
    fav.delete()
    messages.success(request, f" {blog_title}  Deleted")
    return redirect('/home')




@login_required
def my_blogs(request):
    my = Blog.objects.filter(user__exact=request.user)
    recent_blogs = Blog.objects.all().order_by('-created')[:5]


    return render(request, 'my_blogs.html',  {'my': my,'recent_blogs':recent_blogs,})




@login_required
def search_by_blog_title(request):

    search = request.GET['title']
    search = Blog.objects.filter(title__icontains=search)
    recent_blogs = Blog.objects.all().order_by('-created')[:5]

    cat = 'Business'
    cat = Blog.objects.filter(category__icontains=cat)
    print(cat)


    print(search)
    if search == []:
        msg = 'Not found'
        return render(request,"search_by_blog_title.html",{'msg':msg,'recent_blogs':recent_blogs,})
    else:
        return render(request,'search_by_blog_title.html',  {'search': search,'recent_blogs':recent_blogs,})



@login_required()
def profile(request, pk):
    user = User.objects.filter(id=pk)
    user = user.get()
    user_bio = BIO.objects.filter(id=pk)
    form = UserProfileForm (instance=user)



    try:
        avatar = UserProfile.objects.get(user=request.user)

        print(avatar)
        print(user)

        return render(request, 'profile.html', {'user':user,'avatar':avatar,'form':form,'user_bio':user_bio})

    except UserProfile.DoesNotExist:
        avatar = None
        print(avatar)


    return render(request, 'profile.html', {'user':user,'avatar':avatar,'form':form,'user_bio':user_bio})




@login_required()
def upload_profile(request):

    form = UserProfileForm(request.POST or None, request.FILES)
    if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()

            return redirect("/home")
    return redirect("/home")





@login_required()
def remove_img(request,pk):
    img = UserProfile.objects.get(id=pk)
    img.delete()

    return redirect("/home")



@login_required()
def edit_profile(request,pk):
    user = User.objects.filter(id=pk)
    user = user.get()
    form = UserProfileForm(instance=user)
    user_bio = BIO.objects.filter(id=pk)


    formUpdate = UpdateUserForm(instance=user)

    try:
        avatar = UserProfile.objects.get(user=request.user)

        print(avatar)
        print(user)

        return render(request, 'edit_profile.html', {'user': user, 'avatar': avatar, 'form': form,'formUpdate':formUpdate,'user_bio':user_bio})

    except UserProfile.DoesNotExist:
        avatar = None
        print(avatar)

    return render(request, 'edit_profile.html', {'user': user, 'avatar': avatar, 'form': form,'formUpdate':formUpdate,'user_bio':user_bio})



@login_required()
def update_user_info(request):
    if request.method == "POST":
        u_form = UpdateUserForm(instance=request.user, data=request.POST)

        if u_form.is_valid():
            u_form.save()
            messages.success(request, f'Your Profile has been updated!')

    return redirect("/home")






@login_required()
def s_by_Sports(request):
    recent_blogs = Blog.objects.all().order_by('-created')

    cat = 'Sports'
    cat = Blog.objects.filter(category__icontains=cat)
    print(cat)


    if cat == []:
        msg = 'Not found'
        return render(request,"search_by_category.html",{'msg':msg,'recent_blogs':recent_blogs,})
    else:
        return render(request,'search_by_category.html',  {'cat': cat,'recent_blogs':recent_blogs,})



#
#
# @login_required()
# def add_bio(request):
#
#     if request.method == "POST":
#         bio = request.POST.get('bio')
#
#         bio = BIO(bio=bio, user=request.user)
#         bio.save()
#         messages.success(request, f'Your BIO has been updated!')
#
#     return redirect("/home")
#
#
#
#
# @login_required()
# def delete_bio(request,pk):
#     bio = BIO.objects.get(id=pk)
#     bio.delete()
#
#     messages.success(request, f'Your BIO has been deleted!')
#
#     return redirect("/home")

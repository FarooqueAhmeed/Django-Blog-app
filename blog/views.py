from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.
from django.urls import reverse
from .forms import BlogForm, Blog_update_Form
from .models import Blog, Comments, Favorite, Following


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

@login_required()
def home(request):

    blogs = Blog.objects.all()

    context = {'blogs': blogs}

    return render(request, 'home.html',context)


@login_required()
def user(request, pk):

    user = Blog.objects.filter(id=pk)
    user = user.get()
    print(user.user.username)

    get_user = User.objects.get(blog=user)
    print(get_user)

    r_user = User.objects.get(username__exact=request.user)
    print(r_user)


    try:

        check2 = Following.objects.filter(follows=r_user)
        print(check2)

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
            'blog_count':blog_count
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


        context = {
            'check1': check1 ,
            'user':user,
            'get_user':get_user,
             'all_blogs':all_blogs,
            'blog_count':blog_count,
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
    context = {'followed': followed}

    return render(request, 'my_followed.html', context)



@login_required
def unfollow(request, pk):
    boolean_false = Following.objects.get(id=pk)
    boolean_false.delete()

    return redirect('home')




@login_required()
def add_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST or None)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
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



@login_required()
def read_more(request, pk):
    blogs = Blog.objects.filter(id=pk)
    blogs = blogs.get()
    comment = Comments.objects.filter(blog=blogs)

    blogs = Blog.objects.filter(id=pk)

    return render(request, 'read_more.html', {'comment': comment,'blogs':blogs})



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
    favorite.save()
    messages.success(request, f"{blog_title} Blog added to favorites")
    return redirect('home')


@login_required
def favorites(request):
    fav = Favorite.objects.filter(user__exact=request.user)

    return render(request, 'favorites.html',  {'fav': fav})




@login_required
def deletefav(request, pk):
    fav = Favorite.objects.filter(id=pk, ).get()
    blog_title = fav.blog.title
    fav.delete()
    messages.success(request, f" {blog_title}  Deleted")
    return redirect('favorites')



@login_required()
def profile(request, pk):


    user = User.objects.filter(id=pk)
    user = user.get()

    return render(request, 'profile.html', {'user':user})


@login_required
def my_blogs(request):
    my = Blog.objects.filter(user__exact=request.user)

    return render(request, 'my_blogs.html',  {'my': my})















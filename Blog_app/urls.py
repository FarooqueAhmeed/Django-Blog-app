"""Blog_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from blog.views import *
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('home', home, name='home'),
    url(r'^login/$', user_login, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
    url(r'^signup/$', user_signup, name='signup'),

    path('add_blog',add_blog, name='add_blog'),
    path('delete_blog/<int:pk>/',delete_blog, name='delete_blog'),
    path('edit/<int:pk>/', edit, name='edit'),
    path('update/<int:pk>/', update, name='update'),
    path('my_blogs', my_blogs, name='my_blogs'),

    path('read_more/<int:pk>/', read_more, name='read_more'),
    path("comment/<int:pk>", comment, name="comment"),

    path("fav/<int:pk>",fav, name="fav"),
    path('favorites', favorites, name='favorites'),
    path('deletefav/<int:pk>/', deletefav, name='deletefav'),

    path('profile/<int:pk>/', profile, name='profile'),
    path('user/<int:pk>/', user, name='user'),

    path('follow_user/<int:pk>/', follow_user, name='follow_user'),
    path('my_followed', my_followed, name='my_followed'),
    path('unfollow/<int:pk>/', unfollow, name='unfollow'),
    path('my_followers/<int:pk>/', my_followers, name='my_followers'),

    path('search_by_blog_title', search_by_blog_title, name='search_by_blog_title'),

    #path('update_profile/<int:pk>/', update_profile, name='update_profile'),

    path('upload_profile', upload_profile, name='upload_profile'),

    path('remove_img/<int:pk>/', remove_img, name='remove_img'),

    path('edit_profile/<int:pk>/', edit_profile, name='edit_profile'),

    path('update_user_info', update_user_info, name='update_user_info'),

    path('s_by_Sports', s_by_Sports, name='s_by_Sports'),


    # path('add_bio', add_bio, name='add_bio'),

    # path('delete_bio/<int:pk>/', delete_bio, name='delete_bio'),







]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.db import models
from django.contrib.auth.models import User


# Create your models here..
#
# class ExampleModel(models.Model):
#     model_pic = models.ImageField(upload_to = 'blog_image/', default ='media/profile.png')



class UserProfile(models.Model):
    user          = models.OneToOneField(User,on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, blank=True,upload_to="profile_pics",default='profile.png')
    is_avatar = models.BooleanField(default=False, blank=True)
    def __str__(self):
        return '{} {} {}'.format(self.user,'-and image-', self.avatar)

class Blog(models.Model):
    category = (
        ('Sports', 'Sports'),
        ('Business', 'Business'),
        ('Computer', 'Computer'),
        ('Entertainment', 'Entertainment'),
        ('Games', 'Games'),
        ('Family', 'Family'),
        ('Travel', 'Travel'),
        ('Fashion', 'Fashion'),
        ('Politics', 'Politics'),
        ('Pets', 'Pets'),
    )
    category = models.CharField(max_length=13, blank=True,null=True, choices= category)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=1000, null=True,blank=True)
    image = models.ImageField(null=True, blank=True, upload_to="blog_image")
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {} {} {}'.format(self.user,'-blog_title-',self.title, '-image-', self.image)


class Favorite(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return '{} {} {}'.format(self.user,'-fav-', self.blog)


class Comments(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    comment = models.CharField(max_length=250, null=True, default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.comment


class Following(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    a_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follows', blank=True)
    follows = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following', blank=True, default=None)
    boolean = models.BooleanField(default=False,blank=True)

    def __str__(self):

        return '{} {} {} {} {} {} {}'.format(self.a_user,'- following to -' ,self.follows,'-from-',self.created  ,': status =' ,self.boolean)




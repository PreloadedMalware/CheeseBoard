from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
import random
import string

# Create your models here.
class Cheese(models.Model):
    name = models.CharField(max_length = 64)
    slug = models.SlugField(unique = True, default = 'slug')
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Cheese, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Stats(models.Model):
    ID = models.IntegerField(primary_key = True, default = 0)
    timeOnCheeseBoard = models.IntegerField(default = 0)
    posts  = models.IntegerField(default = 0)
    likesTaken = models.IntegerField(default = 0)
    likesGiven = models.IntegerField(default = 0)
    commentsTaken = models.IntegerField(default = 0)
    commentsGiven = models.IntegerField(default = 0)
    cheesesReferenced = models.IntegerField(default = 0)

    def __str__(self):
        return str(self.ID)

class Badge(models.Model):
    name = models.CharField(max_length = 64)

    def __str__(self):
        return self.name
    
class Account(models.Model):
    #username, password, email, forename, surname in user model
    user = models.OneToOneField(User, on_delete=models.CASCADE, editable = True)
    dateOfBirth = models.DateField(default = datetime.today())
    accountCreationDate = models.DateTimeField(default = timezone.now())
    dateLastLoggedIn = models.DateTimeField(default = timezone.now())
    profilePic = models.ImageField(upload_to='profile_images', default='profile_images/default.jpg')
    cheese_points = models.IntegerField(default = 0)
    slug = models.SlugField(unique = True)

    stats = models.OneToOneField(
        Stats,
        on_delete=models.CASCADE,
        primary_key = True,
        unique = False,
    )
    faveCheese = models.ForeignKey(
        Cheese,
        on_delete=models.SET_NULL,
        null = True,
        default = "",
    )
    following = models.ManyToManyField(
        User,
        blank = True,
        null = True,
        related_name='followers2'
    )
    followers = models.ManyToManyField(
        User,
        blank = True,
        null = True,
        related_name='following2'
    )
    badges = models.ManyToManyField(
        Badge,
        blank = True,
        null = True,
    )
    
    def save(self, *args, **kwargs):
        #queryset = Account.objects.filter(slug = self.user.get_username())
        #if queryset == Account.objects.none():
        #    self.slug = slugify(self.user.get_username())
        #super(Account, self).save(*args, **kwargs)
        success = False
        while not success:
            test_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
            queryset = Post.objects.filter(slug = test_slug)
            if not queryset:
                self.slug = slugify(test_slug)
                success = True
        
        super(Account, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.user.get_username())

class Post(models.Model):
    title = models.CharField(max_length = 64, default = "")
    image = models.ImageField(blank = True)
    caption = models.CharField(max_length = 265, default = "")
    body = models.CharField(max_length = 4096, default = "")
    likes = models.IntegerField(default = 0)
    timeDate = models.DateTimeField(default = timezone.now())
    slug = models.SlugField(unique = True)
    
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
        default = "",
    )
    cheeses = models.ManyToManyField(
        Cheese,
        blank = True,
        null=True,
    )
    
    def save(self, *args, **kwargs):
        success = False
        if not self.slug:
            while not success:
                test_slug = ''.join(random.choices(string.ascii_uppercase + string.digits, k=5))
                queryset = Post.objects.filter(slug = test_slug)
                if not queryset:
                    self.slug = slugify(test_slug)
                    success = True
        
        super(Post, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.title

class Saved(models.Model):
    name = models.CharField(max_length = 64)
    posts= models.ManyToManyField(
        Post,
        blank=True,
        null=True,
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null=True,
        default = "",
    )
    def __str__(self):
        return self.name

class Comment(models.Model):
    ID = models.IntegerField(primary_key = True, default = 0)
    likes = models.IntegerField(default = 0)
    body = models.CharField(max_length = 64)
    timeDate = models.DateTimeField(default = timezone.now())
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        null = True,
        default = "",
    )
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        null = True,
        default = "",
    )
    def __str__(self):
        return self.body
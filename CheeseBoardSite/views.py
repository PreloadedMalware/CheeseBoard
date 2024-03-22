from datetime import datetime, timedelta
from django.shortcuts import render, get_object_or_404 
from CheeseBoardSite.models import Account, Comment, Post, Cheese, Stats, Saved
from CheeseBoardSite.forms import CommentForm, SavedForm, UserForm, AccountForm, PostForm, AccountSettingsForm, AccountProfilePicForm
from CheeseBoardSite.models import Account, Post, Cheese, User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Q
import random

def index(request):
    context_dict = {}
    
    
    #most_cheese_points_accounts_list = Account.objects.order_by('-cheese_points')[:10]
    
    context_dict['tags'] = tag_to_list(Post.objects.all().order_by('-timeDate'))  
    context_dict['posts'] = posts_to_list(Post.objects.all())

    most_liked_posts_last_week_list = Post.objects.filter(timeDate__gte =(datetime.now() - timedelta(days=7))).order_by('-likes')[:10]
    if request.user.is_authenticated:
        following_list = request.user.account.following.all()
        latest_posts_from_following_list = Post.objects.order_by('-timeDate')[:10]
        context_dict['followingPosts'] = posts_to_list(latest_posts_from_following_list)
    context_dict['mostLiked'] = posts_to_list(most_liked_posts_last_week_list)
    
    #context_dict['posts'] += posts_to_list(most_cheese_points_accounts_list)
    
    return render(request, 'CheeseBoardSite/index.html', context=context_dict)

def tag_to_list(post_list):
    result_list =[]
    for post in post_list: #last 9 used tags
        for cheese in post.cheeses.all():
            if len(result_list)<10:
                result_list.append(cheese.name)
                result_list = list(set(result_list))
            else:
                break 
    if len(result_list)==0: #if we have nothing to choose from, all cheese types
        cheeses = Cheese.objects.all()
        for cheese in cheeses:
            result_list.append(cheese.name)
    return list(result_list)

def posts_to_list(post_list):
    result_list = []
    for post in post_list:
        result_list.append({
            "title": post.title,
            "content": post.body,
            "img": post.image,
            "slug": post.slug
        })
    return result_list
    

def register(request):
    registered = False

    if request.method == 'POST':
        #try get info
        user_form = UserForm(request.POST)
        account_form = AccountForm(request.POST)
    
        if user_form.is_valid() and account_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            account = account_form.save(commit=False)
            account.user = user
            account.accountCreationDate = timezone.now()
            account.dateLastLoggedIn = timezone.now()
            made = False
            while not made:
                s,m=Stats.objects.get_or_create(ID = random.randint(0,999999999))
                if m:
                    made = True
            s.save()
            account.stats = s
            # if 'profilePic' in request.FILES:
            #     account.profilePic = request.FILES['profilePic']
            
            account.save()
            registered = True
            return redirect("/")

        else:
            print(user_form.errors, account_form.errors)
    else:
        # not http post, use empty form for user input
        user_form = UserForm()
        account_form = AccountForm()

    return render(request, 'CheeseBoardSite/register.html',
                  context = {'user_form': user_form,
                             'account_form': account_form,
                             'registered': registered})
    
# ADD CHANGE DETAILS FORM -- SEE ACCOUNT.HTML FOR FIELDS REQUIRED -- BASIS STARTED IN edit_account VIEW
@login_required
def account(request):
    if request.user.is_authenticated:
        userAccount = Account.objects.get(user = request.user)
        user_posts = Post.objects.filter(account = userAccount)
        user_posts_list = posts_to_list(user_posts)
        edit_form = AccountSettingsForm(initial={
            'username': request.user.username,
            'email': request.user.email,
            'forename': request.user.first_name,
            'surname': request.user.last_name,
        })
        pfp_form = AccountProfilePicForm()
        context_dict = {
            "username": request.user.username,
            "email": request.user.email,
            "forename": request.user.first_name,
            "surname": request.user.last_name,
            "dateOfBirth": userAccount.dateOfBirth,
            "accountCreationDate": userAccount.accountCreationDate,
            "dateLastLoggedIn": userAccount.dateLastLoggedIn,
            "profilePic": userAccount.profilePic,
            "stats": userAccount.stats,
            "faveCheese": userAccount.faveCheese,
            "followers": userAccount.followers.count,
            "following": userAccount.following.count,
            "cheese_point" : userAccount.cheese_points,
            "badges": userAccount.badges,
            "is_account_holder": (userAccount.user == request.user),
            "posts": user_posts_list,
            "edit_form": edit_form,
            "pfp_form": pfp_form,
        }

        return render(request, 'CheeseBoardSite/account.html', context=context_dict)
    else:
        return redirect(reverse('CheeseBoardSite:login'))


def user_login(request):
    if request.method == 'POST':
        # try get info
        username = request.POST.get('username')
        password = request.POST.get('password')

        isValidLogin = authenticate(username=username, password=password)

        if isValidLogin:
            if isValidLogin.is_active:
                # if valid account is active log them back in
                login(request, isValidLogin)
                return redirect(reverse('CheeseBoardSite:index'))
            else:
                # account is inactive
                return HttpResponse("Account is disabled.")
        else:
            # not valid login details
            print(f"Login details are incorrect.")
            return HttpResponse("Incorrect Login details.")
    else:
        # not a http post
        return render(request, 'CheeseBoardSite/login.html')


@login_required
def user_logout(request):
    logout(request)
    # go back to homepage
    return redirect(reverse('CheeseBoardSite:index'))

def search(request, query):
    context_dict = {}
    context_dict['term'] = query
    
    prepositions =('above', 'across', 'after', 'against', 'along', 'among', 'around', 'at', 'about',
                    'before', 'behind', 'below', 'beneath', 'beside', 'between', 'beyond', 'but', 'by',
                    'concerning', 'considering', 'despite', 'down', 'during', 'except', 'for', 'from', 
                    'in', 'inside', 'into', 'like', 'near', 'of', 'off', 'on', 'onto', 'out', 'outside', 
                    'over', 'past', 'regarding', 'since', 'through', 'throughout', 'till', 'to',
                    'toward', 'under', 'underneath', 'until', 'up', 'upon', 'with', 'within', 'without', 'a', 'the')
    query = ' '.join(set(query.split()).difference(prepositions))
    posts = Post.objects.filter(
        Q(title__icontains=query) | 
        Q(body__icontains=query) |
        Q(cheeses__name__icontains=query) 
    ).distinct()    
    context_dict['posts'] = posts_to_list(posts)
    context_dict['tags'] = tag_to_list(Post.objects.all().order_by('-timeDate'))
    return render(request, 'CheeseBoardSite/search.html', context=context_dict)

# ADD FOLLOW FORM
def view_page(request, slug):
    if slug:
        account_slug = slug
        account = Account.objects.get(slug=account_slug)
        user_posts = Post.objects.filter(account = account)
        user_posts_list = posts_to_list(user_posts)
        context_dict ={
            'username' : account.user.username,
            'profilePic' : account.profilePic,          
            "stats": account.stats,
            "faveCheese": account.faveCheese,
            "followers": account.followers.count(),
            "following": account.following,
            "badges": account.badges,
            "is_account_holder": (account.user == request.user),
            "posts": user_posts_list,
        }
        #follow(request, account.user,False)

    return render(request, 'CheeseBoardSite/account.html', context=context_dict)  #WHAT HTML

@login_required
def edit_page(request):
    account = get_object_or_404(Account, user=request.user)

    if request.method == 'POST':
        form = AccountSettingsForm(request.POST, instance=account.user)
        pfp_form = AccountProfilePicForm(request.POST, request.FILES, instance=account)
        print(form.errors)
        if form.is_valid() and pfp_form.is_valid():
            print(account.user)
            account.user = form.save()
            # request.user= user
            if len(request.FILES) > 0:
                account = pfp_form.save()         
    return redirect('CheeseBoardSite:account')


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.account = request.user.account  
            post.timeDate = timezone.now()  
            request.user.account.stats.posts += 1
            post.likes = 0  
            post.save()
            form.save_m2m()
            return redirect('/')  
    else:
        form = PostForm()
    return render(request, 'CheeseBoardSite/create_post.html', {'post_form': form})
    
# ADD LIKE AND SAVE FORMS
def view_post(request, slug):
    if slug:
        post_slug = slug
        post = Post.objects.get(slug=post_slug)
        context_dict = {
            'title' : post.title,
            'image' : post.image,
            'caption' : post.caption,
            'body' : post.body,
            'likes' : post.likes,
            'timeDate' : post.timeDate,
            'account' : post.account,
            'slug': post.slug,
            'cheeses': post.cheeses.all(),
            'comments' : Comment.objects.filter(post = post),
            'saved_form': SavedForm(),
        }
        context_dict["comment_form"]=comment_post(request, slug)
        if request.method == 'POST':
            print(request.POST.get('body'))
        return render(request, 'CheeseBoardSite/post.html', context = context_dict)
    

@login_required
def follow(request, follow_user, option): ##    FOR FOLLOWING OPTION=TRUE, FOR UNFOLLOWING OPTION = FALSE
    account_user = request.user
    account = Account.objects.get(user = account_user)
    follow = Account.objects.get(user = follow_user)
    if follow == None:
        return redirect(reverse('CheeseBoardSite:index'))
    if option:        
        account.following.add(follow.user)
        follow.followers.add(account.user)
    elif not option:
        account.following.remove(follow.user)
        follow.followers.remove(account.user)
    return redirect('CheeseBoardSite:view_page', slug=follow.slug)

@login_required
def like_post(request, slug):
    if slug:
        post_slug = slug
        post = Post.objects.get(slug=post_slug)
        post.likes +=1
        post.save()
        account = Account.objects.get(user = request.user)
        account.stats.likesGiven +=1
        account.save() 
        account = Account.objects.get(user =  post.account.user)
        account.stats.likesTaken +=1
        account.save()        
    return redirect('CheeseBoardSite:view_post', slug=slug)

@login_required
def comment_post(request, slug):
    if slug:
        post_slug = slug
        post = Post.objects.get(slug=post_slug)
        account = Account.objects.get(user = request.user)
        account.stats.commentsGiven +=1
        account.save()    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.ID = Comment.objects.count() + 1
            comment.body = request.POST.get('body')
            comment.post = post
            comment.account = account
            comment.save()
            return form 
    else:
        form = CommentForm()      
    return form   

@login_required
def like_comment(request,slug):
        comment = Comment.objects.get(ID = id)
        comment.likes +=1
        comment.save()
        return redirect('CheeseBoardSite:view_post', slug=slug)
    
@login_required
def save_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == 'POST':
        form = SavedForm(request.POST)
        if form.is_valid():
            name = f"{request.user.username}'s posts"
            saved, created = Saved.objects.get_or_create(name=name, account=Account.objects.get(user=request.user))
            saved.posts.add(post)
            saved.save()
    return redirect('CheeseBoardSite:view_post', slug=slug)

from django.urls import path
from CheeseBoardSite import views
from django.contrib.auth.views import LogoutView

app_name = 'CheeseBoardSite'
urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    # add this url to a button to logout
    path('logout/', views.user_logout, name='logout'),
    path('account', views.account, name='account'),
    path('account/edit', views.edit_page, name='edit_page'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/<str:query>/', views.search, name='search'),
    path('profile/<slug:slug>/', views.view_page, name = 'view_page'),
    path('profile/<slug:slug>/follow', views.follow_unfollow_account, name='follow'),
    path('post/<slug:slug>/', views.view_post, name = 'view_post'),
    path('post/<slug:slug>/save', views.save_post, name='save_post'),
    path('post/<slug:slug>/like', views.like_post, name='like_post'),
    path('post/<slug:slug>/comment', views.comment_post, name='comment_post'),
    path('post/<slug:slug>/like', views.like_comment, name='like_comment'),
]

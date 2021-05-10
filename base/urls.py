from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.posts, name="posts"),
    path('my_posts/', views.my_posts, name="my_posts"),
    path('post/<slug:slug>/', views.post, name="post"),

    # CRUD PATHS

    path('create_post/', views.createPost, name="create_post"),
    path('update_post/<slug:slug>/', views.updatePost, name="update_post"),
    path('delete_post/<slug:slug>/', views.deletePost, name="delete_post"),

    path('send_email/', views.sendEmail, name="send_email"),

    path('login/', views.loginPage, name="login"),
    path('register/', views.registerPage, name="register"),
    path('logout/', views.logoutUser, name="logout"),

    path('profile/<slug:slug>/', views.profile, name="profile"),
    path('update_profile/', views.updateProfile, name="update_profile"),

    path('chat/<slug:slug>/', views.chat, name="chat"),

    path('chats/', views.chats, name="chats"),


]
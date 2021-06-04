from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('posts/', views.posts, name="posts"),
    path('post/<slug:slug>/', views.post, name="post"),

    # CRUD PATHS

    path('create_post/', views.createPost, name="create_post"),
    path('update_post/<slug:slug>/', views.updatePost, name="update_post"),
    path('delete_post/<slug:slug>/', views.deletePost, name="delete_post"),

    path('add_order/<slug:slug>', views.addOrder, name="add_order"),
    path('orders', views.orders, name="orders"),
    path('orderDelete/<int:id>/', views.orderDelete, name="orderDelete"),

    path('profile/<str:username>/', views.profile, name="profile"),
    path('update_profile/', views.updateProfile, name="update_profile"),
    path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('createChat/<str:username>/', views.createChat, name="createChat"),
    path('chat/<int:id>/', views.chat, name="chat"),
    path('chats/', views.chats, name="chats"),
    path('send_email/', views.sendEmail, name="send_email"),
    path('admin_page', views.admin_page, name="admin_page"),
    path('category', views.category, name="category"),
    path('categoryDelete/<int:id>/', views.categoryDelete, name="categoryDelete"),
    path('add_category/', views.add_category, name="add_category"),
    path('category_edit/<int:id>/', views.category_edit, name="category_edit"),
    path('category_posts/<str:name>/', views.category_posts, name="category_posts"),
    path('posts_comments', views.posts_comments, name="posts_comments"),
    path('update_post_comment/<int:id>/', views.updatePostComment, name="update_post_comment"),
    path('commentPostDelete/<int:id>/', views.commentPostDelete, name="commentPostDelete"),
    path('profiles_comments', views.profiles_comments, name="profiles_comments"),
    path('commentProfileDelete/<int:id>/', views.commentProfileDelete, name="commentProfileDelete"),
    path('update_profile_comment/<int:id>/', views.updateProfileComment, name="update_profile_comment"),
    path('users', views.users, name="users"),
    path('usersDelete/<int:id>/', views.usersDelete, name="usersDelete"),

    path('delete_post_admin/<slug:slug>/', views.deletePostAdmin, name="delete_post_admin"),
    path('posts_admin', views.posts_admin, name="posts_admin"),

    path('usersDelete/<int:id>/', views.usersDelete, name="usersDelete"),
    path('postsDelete/<int:id>/', views.postsDelete, name="postsDelete"),
    path('letter/<int:id>/', views.letter, name="letter"),
    path('letters', views.letters, name="letters"),

    path('letterDelete/<int:id>/', views.letterDelete, name="letterDelete"),

]

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .decorators import admin_only

from .forms import PostForm, CustomUserCreationForm, ProfileForm, UserForm, PostCommentForm, ProfileCommentForm, \
    CategoryForm
from .filters import PostFilter, PostFilterName
from .models import *


def posts(request):
    posts = Post.objects.filter(active=True).order_by('-created')
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, 'base/posts.html', context)


def home(request):
    posts = Post.objects.filter(active=True).order_by('-created')
    myFilter = PostFilterName(request.GET, queryset=posts)
    posts = myFilter.qs
    tags = Tag.objects.all()
    page = request.GET.get('page')
    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'myFilter': myFilter, 'tags': tags}
    return render(request, 'base/index.html', context)


def post(request, slug):
    post = Post.objects.get(slug=slug)
    images = Image.objects.filter(condo=post)
    if request.method == 'POST':
        PostComment.objects.create(
            author=request.user.profile,
            post=post,
            body=request.POST['comment']
        )
        return redirect('post', slug=post.slug)
    context = {'post': post, 'images': images}
    return render(request, 'base/post.html', context)


@login_required(login_url="home")
def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user.profile
            post.save()
        for file in request.FILES.getlist('images'):
            instance = Image(
                condo=post,
                image=file
            )
            instance.save()
        return redirect('posts')
    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="home")
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        for file in request.FILES.getlist('images'):
            instance = Image(
                condo=post,
                image=file
            )
            instance.save()
        return redirect('posts')
    context = {'form': form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="home")
def deletePost(request, slug):
    deletePost = Post.objects.filter(slug=slug)
    if request.method == 'POST':
        deletePost.delete()
        return redirect('posts')
    context = {'item':deletePost}
    return render(request, 'base/delete.html', context)


def sendEmail(request):
    if request.method == 'POST':
        instance = Letter(name=request.POST['name'], theme=request.POST['subject'],
                          email=request.POST['email'], message=request.POST['message'])
        instance.save()
        return redirect('posts')
    return render(request, 'base/email_sent.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'Не вірний е-mail або пароль')
            return redirect('login')
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Не вірний е-mail або пароль')
    context = {}
    return render(request, 'base/login.html', context)


def registerPage(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            profile = Profile(user=user)
            profile.save()
            messages.success(request, 'Акаунт створено!')
            user = authenticate(request, username=user.username, password=request.POST['password1'])
            if user is not None:
                login(request, user)
            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'Помилка реєстрації')
    context = {'form': form}
    return render(request, 'base/register.html', context)


@login_required(login_url="home")
def logoutUser(request):
    logout(request)
    return redirect('home')


def profile(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    posts = Post.objects.filter(active=True, author=user.profile).order_by('-created')
    page = request.GET.get('page')
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        ProfileComment.objects.create(
            author=request.user.profile,
            profile=profile,
            body=request.POST['comment']
        )
        return redirect('profile', username=user.username)
    context = {'user': user, 'posts': posts}
    return render(request, 'base/profile.html', context)


@login_required(login_url="home")
def updateProfile(request):
    user = request.user
    profile = user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        user_form = UserForm(request.POST, instance=user)
        if user_form.is_valid():
            user_form.save()
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=user.username)
    context = {'form': form}
    return render(request, 'base/profile_form.html', context)


@login_required(login_url="home")
def createChat(request, username):
    user = User.objects.get(username=username)
    profile = Profile.objects.get(user=user)
    if Chat.objects.filter(sender=request.user.profile, recipient=profile).exists():
        chat = Chat.objects.get(sender=request.user.profile, recipient=profile)
        return redirect('chat', id=chat.id)
    else:
        chat = Chat(
            sender=request.user.profile, recipient=profile
        )
        chat.save()
        chat = Chat.objects.get(sender=request.user.profile, recipient=profile)
        return redirect('chat', id=chat.id)


@login_required(login_url="home")
def chat(request, id):
    user2 = request.user.profile
    chat = Chat.objects.get(id=id)
    chats = Chat.objects.all()
    if request.method == 'POST':
        mes = Message(
            send=user2,
            chat=chat,
            body=request.POST['comment']
        )
        mes.save()
    messag = Message.objects.filter(chat=chat).order_by('-created')
    context = {'chat': chat, 'chats': chats, 'messag': messag}
    return render(request, 'base/chat.html', context)


@login_required(login_url="home")
def chats(request):
    chats = Chat.objects.filter(sender=request.user.profile) | Chat.objects.filter(recipient=request.user.profile)
    page = request.GET.get('page')
    paginator = Paginator(chats, 5)
    try:
        chats = paginator.page(page)
    except PageNotAnInteger:
        chats = paginator.page(1)
    except EmptyPage:
        chats = paginator.page(paginator.num_pages)
    context = {'chats': chats}
    return render(request, 'base/chats.html', context)


@login_required(login_url="home")
def addOrder(request, slug):
    post = Post.objects.get(slug=slug)
    if not Order.objects.filter(post=post, customer=request.user.profile).exists():
        Order.objects.create(
            customer=request.user.profile,
            post=post,
            status=False,
        )
        messages.success(request,
                         "Ви успішно додали дане оголошення до вподобаних.")
        return redirect('post', slug=post.slug)
    else:
        messages.error(request, "Це оголошення ви вже додали до списку замовлень.")
        return redirect('post', slug=post.slug)


@login_required(login_url="home")
def orders(request):
    orders = Order.objects.filter(customer=request.user.profile)
    page = request.GET.get('page')
    paginator = Paginator(orders, 6)
    try:
        orders = paginator.page(page)
    except PageNotAnInteger:
        orders = paginator.page(1)
    except EmptyPage:
        orders = paginator.page(paginator.num_pages)
    context = {'orders': orders}
    return render(request, 'base/orders.html', context)


@admin_only
@login_required(login_url="home")
def admin_page(request):
    return render(request, 'base/admin_page.html')


@admin_only
@login_required(login_url="home")
def users(request):
    profiles = Profile.objects.all()
    context = {'profiles': profiles}
    return render(request, 'base/users.html', context)


@admin_only
@login_required(login_url="home")
def deletePostAdmin(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item': post}
    return render(request, 'base/delete_admin.html', context)


@admin_only
@login_required(login_url="home")
def posts_admin(request):
    posts = Post.objects.filter(active=True)
    context = {'posts': posts}
    return render(request, 'base/posts_admin.html', context)


@admin_only
@login_required(login_url="home")
def posts_comments(request):
    comments = PostComment.objects.all()
    context = {'comments': comments}
    return render(request, 'base/posts_comments.html', context)


@admin_only
@login_required(login_url="home")
def profiles_comments(request):
    comments = ProfileComment.objects.all()
    context = {'comments': comments}
    return render(request, 'base/profiles_comments.html', context)


@admin_only
@login_required(login_url="home")
def letters(request):
    letters = Letter.objects.all()
    context = {'letters': letters}
    return render(request, 'base/letters.html', context)


@admin_only
@login_required(login_url="home")
def category(request):
    category = Tag.objects.all()
    context = {'categories': category}
    return render(request, 'base/categories.html', context)


@admin_only
@login_required(login_url="home")
def categoryDelete(request, id):
    deleteCat = Tag.objects.filter(id=id)
    deleteCat.delete()
    return redirect('category')


@admin_only
@login_required(login_url="home")
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()

        return redirect('category')
    context = {'form': form}
    return render(request, 'base/category_form.html', context)


@admin_only
@login_required(login_url="home")
def category_edit(request, id):
    cat = Tag.objects.get(id=id)
    form = CategoryForm(instance=cat)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            form.save()
        return redirect('category')
    context = {'form': form}
    return render(request, 'base/category_form.html', context)


@admin_only
@login_required(login_url="home")
def letterDelete(request, id):
    deleteLet = Letter.objects.filter(id=id)
    deleteLet.delete()
    return redirect('letters')


@login_required(login_url="home")
def orderDelete(request, id):
    deleteOrder = Order.objects.filter(id=id)
    deleteOrder.delete()
    return redirect('orders')


@admin_only
@login_required(login_url="home")
def commentProfileDelete(request, id):
    deleteCom = ProfileComment.objects.filter(id=id)
    deleteCom.delete()
    return redirect('profiles_comments')


@admin_only
@login_required(login_url="home")
def commentPostDelete(request, id):
    deleteCom = PostComment.objects.filter(id=id)
    deleteCom.delete()
    return redirect('posts_comments')


@admin_only
@login_required(login_url="home")
def usersDelete(request, id):
    deleteUs = Profile.objects.filter(id=id)
    deleteUs.delete()
    return redirect('users')


@admin_only
@login_required(login_url="home")
def postsDelete(request, id):
    deletePost = Post.objects.filter(id=id)
    deletePost.delete()
    return redirect('posts_admin')


@admin_only
@login_required(login_url="home")
def letter(request, id):
    letter = Letter.objects.get(id=id)
    context = {'letter': letter}
    return render(request, 'base/letter.html', context)


def category_posts(request, name):
    tags = Tag.objects.filter(name=name)
    posts = Post.objects.filter(tags=tags[0])
    myFilter = PostFilterName(request.GET, queryset=posts)
    posts = myFilter.qs
    page = request.GET.get('page')
    paginator = Paginator(posts, 6)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {'posts': posts, 'myFilter': myFilter, 'name': name}
    return render(request, 'base/category_posts.html', context)


@login_required(login_url="home")
def updatePostComment(request, id):
    comment = PostComment.objects.get(id=id)
    form = PostCommentForm(instance=comment)
    if request.method == 'POST':
        form = PostCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()

        return redirect('post', slug=comment.post.slug)

    context = {'form': form, 'comment': comment}
    return render(request, 'base/postComment_form.html', context)


@login_required(login_url="home")
def updateProfileComment(request, id):
    comment = ProfileComment.objects.get(id=id)
    form = ProfileCommentForm(instance=comment)
    if request.method == 'POST':
        form = ProfileCommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
        return redirect('profile', username=comment.author.user.username)
    context = {'form': form, 'comment': comment}
    return render(request, 'base/profileComment_form.html', context)

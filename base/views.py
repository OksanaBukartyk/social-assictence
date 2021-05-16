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
from .decorators import *

from .forms import PostForm, CustomUserCreationForm, ProfileForm, UserForm
from .filters import PostFilter, PostFilterName

from .models import *


# Create your views here.
def posts(request):
    posts = Post.objects.filter(active=True).order_by('-created')
    myFilter = PostFilterName(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')

    paginator = Paginator(posts, 3)
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

    page = request.GET.get('page')

    paginator = Paginator(posts, 3)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}
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
        messages.success(request, "You're comment was successfuly posted!")

        return redirect('post', slug=post.slug)

    context = {'post': post, 'images': images}
    return render(request, 'base/post.html', context)


def my_posts(request):
    posts = Post.objects.filter(active=True, author=request.user.profile).order_by('-created')
    myFilter = PostFilter(request.GET, queryset=posts)
    posts = myFilter.qs

    page = request.GET.get('page')

    paginator = Paginator(posts, 5)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'myFilter': myFilter}
    return render(request, 'base/posts.html', context)


# CRUD VIEWS
#@admin_only
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


@admin_only
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


@admin_only
@login_required(login_url="home")
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item': post}
    return render(request, 'base/delete.html', context)


def sendEmail(request):
    if request.method == 'POST':
        template = render_to_string('base/email_template.html', {
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })

        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['oksana.petriv17@gmail.com']
        )

        email.fail_silently = False
        email.send()

    return render(request, 'base/email_sent.html')


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Little Hack to work around re-building the usermodel
        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except:
            messages.error(request, 'User with this email does not exists')
            return redirect('login')

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Email OR password is incorrect')

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
            messages.success(request, 'Account successfuly created!')

            user = authenticate(request, username=user.username, password=request.POST['password1'])

            if user is not None:
                login(request, user)

            next_url = request.GET.get('next')
            if next_url == '' or next_url == None:
                next_url = 'home'
            return redirect(next_url)
        else:
            messages.error(request, 'An error has occured with registration')
    context = {'form': form}
    return render(request, 'base/register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')


def profile(request, username):
    user=User.objects.get(username=username)
    profile = Profile.objects.get(user = user)
    chats = (Chat.objects.filter(sender=request.user.profile, recipient=user.profile) |
             Chat.objects.filter(sender=user.profile, recipient=request.user.profile)).first()
    posts = Post.objects.filter(active=True, author=request.user.profile).order_by('-created')

    page = request.GET.get('page')

    paginator = Paginator(posts, 6)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    """if chats == None:
        chats = Chat.objects.create(
            sender=request.user.profile,
            recipient=profile)
"""
    if request.method == 'POST':
        ProfileComment.objects.create(
            author=request.user.profile,
            profile=profile,
            body=request.POST['comment']
        )
        messages.success(request, "You're comment was successfuly posted!")

        return redirect('profile', username=user.username)

    context = {'user': user, 'chats': chats, 'posts': posts}

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


def chat(request, slug):
    user2 = request.user.profile
    chat = Chat.objects.get(slug=slug)

    if request.method == 'POST':
        Message.objects.create(
            send=user2,
            chat=chat,
            body=request.POST['comment']
        )
        messages.success(request, "You're message was successfuly posted!")

        return redirect('chat', slug=chat.slug)

    context = {'chat': chat}
    return render(request, 'base/chat.html', context)


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


class DialogsView():
    def get(self, request):
        chats = Chat.objects.filter(members__in=[request.user.id])
        return render(request, 'users/dialogs.html', {'user_profile': request.user, 'chats': chats})


def addOrder(request, slug):
    post = Post.objects.get(slug=slug)
    #order=Order.objects.пуе(post=post, customer=request.user.profile)
    if not Order.objects.filter(post=post, customer=request.user.profile).exists():
        Order.objects.create(
                customer=request.user.profile,
                post=post,
                status=False,
            )
        messages.success (request, "You're order was successfuly added!")

        return redirect('post', slug=post.slug)
    else:
        messages.error(request, "Уже там ")
        return redirect('post', slug=post.slug)


def orders(request):
    posts = Order.objects.filter(status=False, customer=request.user.profile)



    page = request.GET.get('page')

    paginator = Paginator(posts, 1)

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts}
    return render(request, 'base/orders.html', context)


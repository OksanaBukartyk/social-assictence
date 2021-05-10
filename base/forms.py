from django.db.models import Prefetch
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .fields import GroupedModelChoiceField
import django_filters
from django_filters import CharFilter

from .models import Post, Profile, Tag


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        #fields = ['headline', 'thumbnail', 'tags', 'body']
        labels = {'headline': ('Назва'), 'thumbnail': ('Основне фото'), 'body': ('Опис'), 'tags': ('Категорія')}
        help_texts = {'headline': ('Коротко і ясно'), 'thumbnail': ('Буде показано в пошуку'),
                      'body': ('Детальна інформація про товар')}


        exclude = ['author', 'slug', 'active', 'featured']
        # fields = ['headline', 'tags', 'author', 'product_category', ]


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        labels = {'first_name': ("Ім'я"), 'last_name': ('Прізвище'), 'email': ('E-mail'),
                  'profile_pic': ('Аватарка'), 'bio': ('Біографія')}
        help_texts = {'bio': ('Основна інформація про вас, необхідна для знайомства з вами.')}
        exclude = ['user', 'slug']

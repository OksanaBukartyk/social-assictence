from django.db.models import Prefetch
from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .fields import GroupedModelChoiceField
import django_filters
from django_filters import CharFilter

from .models import Post, Profile, Tag, ProfileComment,PostComment


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User

        fields = ['username', 'email', 'password1', 'password2']
        labels = {'username': ("Ім'я користувача"), 'email': ('Електронна пошта*'), 'password1': ('Пароль'),
                  'password2': ('Пароль (повторно)')}
        help_texts = {'username': ('Letters A-Z or a-z, digits 0-9 and @/./+/-/_ only.')}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Це поле є обов'язковим")
        return email


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'
        # fields = ['headline', 'thumbnail', 'tags', 'body']
        labels = {'headline': ('Назва'), 'thumbnail': ('Основне фото'), 'body': ('Опис'), 'type': ('Стан'),
                  'tags': ('Категорія'), 'address': ('Місто/cело/смт:')}
        help_texts = {'headline': ('Коротко і ясно'), 'thumbnail': ('Буде показано в пошуку'),
                      'body': ('Детальна інформація про товар')}

        exclude = ['author', 'slug', 'active', 'featured']
        # fields = ['headline', 'tags', 'author', 'product_category', ]


class CategoryForm(ModelForm):
    class Meta:
        model = Tag
        fields = '__all__'
        # fields = ['headline', 'thumbnail', 'tags', 'body']
        labels = {'name': ('Назва'), 'image': ('Основне фото')}




class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        labels = {
                  'profile_pic': ('Аватарка'), 'bio': ('Біографія')}
        help_texts = {'bio': ('Основна інформація про вас, необхідна для знайомства з вами.')}
        exclude = [ 'user', 'email','slug']


class PostCommentForm(ModelForm):
    class Meta:
        model = PostComment
        fields = '__all__'
        exclude = ['author']
        # fields = ['headline', 'thumbnail', 'tags', 'body']


class ProfileCommentForm(ModelForm):
    class Meta:
        model = ProfileComment
        fields = '__all__'
        exclude = ['author', 'profile']
        # fields = ['headline', 'thumbnail', 'tags', 'body']

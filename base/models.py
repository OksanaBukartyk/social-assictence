from datetime import timezone

from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.template.defaultfilters import slugify as django_slugify

alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    #first_name = models.CharField(max_length=200, blank=True, null=True)
    #last_name = models.CharField(max_length=200, blank=True, null=True)
    #email = models.CharField(max_length=200)
    #phone=models.CharField(max_length=13)
    profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default="user.png")
    bio = models.TextField(null=True, blank=True)
    last_visit = models.DateTimeField(auto_now_add=True)


class Tag(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="images", blank=False, null=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    headline = models.CharField(max_length=30, blank=False, null=False)
    thumbnail = models.ImageField(upload_to="images", blank=False, null=False)
    body = models.TextField(max_length=500, null=False, blank=False)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    featured = models.BooleanField(default=False)
    tags = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, default=1)
    slug = models.SlugField(null=True, blank=True)
    type = models.CharField(max_length=8, choices=(("Вживаний", ("Вживаний")),
                                     ("Новий", ("Новий"))),
                            default="Вживаний")
    address = models.CharField(max_length=100, null=False, blank=False, default=None)


    def __str__(self):
        return self.headline

    def save(self, *args, **kwargs):
        if self.slug == None:
            slug = slugify(self.headline)
            has_slug = Post.objects.filter(slug=slug).exists()
            count = 1
            while has_slug:
                count += 1
                slug = slugify(self.headline) + '-' + str(count)
                has_slug = Post.objects.filter(slug=slug).exists()
            self.slug = slug
        super().save(*args, **kwargs)


class PostComment(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now


class ProfileComment(models.Model):
    author = models.ForeignKey(Profile, related_name='author', on_delete=models.CASCADE, null=True, blank=True)
    profile = models.ForeignKey(Profile, related_name='profiles', on_delete=models.CASCADE, null=True, blank=True)
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now


class Image(models.Model):
    condo = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to="images/")
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now


class Chat(models.Model):
    sender = models.ForeignKey(Profile, related_name='sender', on_delete=models.CASCADE, null=True, blank=True)
    recipient = models.ForeignKey(Profile, related_name='recipient', on_delete=models.CASCADE, null=True, blank=True)



class Message(models.Model):
    chat = models.ForeignKey(Chat, related_name='chats', on_delete=models.CASCADE, null=True, blank=True)
    send = models.ForeignKey(Profile, related_name='send', on_delete=models.CASCADE, null=True, blank=True)
    body = RichTextUploadingField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.body

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now

class Order(models.Model):
    post = models.ForeignKey(Post, related_name='post', on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Profile, related_name='customer', on_delete=models.CASCADE, null=True, blank=True)
    status = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now

class Letter(models.Model):
    name=models.TextField(null=True, blank=True)
    theme =models.TextField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message=models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def created_dynamic(self):
        now = timezone.now()
        return now



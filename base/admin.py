from django.contrib import admin

# Register your models here.

from .models import *


admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(Tag)
admin.site.register(PostComment)
admin.site.register(ProfileComment)
admin.site.register(Image)
admin.site.register(Chat)
admin.site.register(Message)



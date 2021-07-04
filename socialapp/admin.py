from django.contrib import admin
from socialapp.models import Post, Like


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass

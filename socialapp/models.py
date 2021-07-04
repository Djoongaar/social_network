from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    title = models.CharField(verbose_name='Title', max_length=64)
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def count_likes(self):
        """ Return number of likes for specific Post object """
        return self.likes.select_related().count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        default_related_name = 'likes'

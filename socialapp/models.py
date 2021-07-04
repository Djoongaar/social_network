from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Post(models.Model):
    title = models.CharField(verbose_name='Title', max_length=64)
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, related_name='users_likes', through='Like')

    @property
    def count_likes(self):
        return self.preferences.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, related_name='preferences', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)

    class Meta:
        """ Surrogate Primary Key: Restriction from creating duplicate likes """
        unique_together = (('user', 'post'),)

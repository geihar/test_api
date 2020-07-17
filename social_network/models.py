from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify



class User(models.Model):
    pass


class Post(models.Model):
    title = models.CharField(max_length=120, verbose_name='Тема поста')
    content = models.TextField(verbose_name='Тело поста')
    slug = models.SlugField()
    creation_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Post, self).save(*args, **kwargs)
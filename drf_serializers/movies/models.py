from django.contrib.auth.models import User
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    release_date = models.DateField()
    rating = models.PositiveSmallIntegerField()

    us_gross = models.IntegerField(default=0)
    worldwide_gross = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.title}'


class Resource(models.Model):
    title = models.CharField(max_length=256)
    content = models.TextField()
    liked_by = models.ManyToManyField(User)

    def __str__(self):
        return self.title
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    birth_date = models.DateField()

    def __str__(self):
        return f'{self.user.username} profile'


class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime = models.DateTimeField(auto_now_add=True)
    content = models.TextField()


class ModelC(models.Model):
    content = models.CharField(max_length=128)


class ModelB(models.Model):
    model_c = models.ForeignKey(ModelC, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)


class ModelA(models.Model):
    model_b = models.ForeignKey(ModelB, on_delete=models.CASCADE)
    content = models.CharField(max_length=128)
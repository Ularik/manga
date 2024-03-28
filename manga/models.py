from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='rating'
    )
    grade = models.DecimalField(
        max_digits=2,
        decimal_places=1
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )


class Likes(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )


class Comments(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.CharField(
        max_length=100
    )


class Genre(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()


class Image(models.Model):
    file = models.ImageField(upload_to='media/mangas/')


class Manga(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    title = models.CharField(
        max_length=100
    )
    description = models.TextField()
    genre = models.ManyToManyField(Genre)
    images = models.ManyToManyField(Image)
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True
    )


class WatchManga(models.Model):
    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE,
        related_name='watches'
    )
    created_date = models.DateTimeField(
        auto_now=True
    )
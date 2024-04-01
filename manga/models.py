from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Rating(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
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
        related_name='favorites',
    )
    manga = models.ForeignKey(
        'Manga',
        on_delete=models.CASCADE,
        related_name='likes'
    )
    created_date = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.user} -> {self.manga}'


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

    def __str__(self):
        return self.title


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
    images = models.ImageField(
        upload_to='media/cover',
        null=True,
        blank=True
    )
    grades = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        null=True,
        blank=True
    )
    comix_file = models.FileField(upload_to='media/comix')
    created_date = models.DateTimeField(
        auto_now_add=True
    )
    updated_date = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.title


class Watched(models.Model):
    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE,
        related_name='watches'
    )
    created_date = models.DateTimeField(
        auto_now=True
    )


class Bookmarks(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    manga = models.ForeignKey(
        Manga,
        on_delete=models.CASCADE,
        related_name='bookmarks'
    )

    def __str__(self):
        return f'{self.user.name}: {self.manga.title}'
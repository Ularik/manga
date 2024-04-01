from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Manga)
admin.site.register(models.Genre)
admin.site.register(models.Comments)
admin.site.register(models.Rating)
admin.site.register(models.Likes)
admin.site.register(models.Bookmarks)
admin.site.register(models.Watched)



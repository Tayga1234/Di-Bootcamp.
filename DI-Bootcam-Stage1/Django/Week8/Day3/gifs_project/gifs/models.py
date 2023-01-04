from django.db import models

class Gif(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    uploader_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(max_length=255)
    gifs = models.ManyToManyField(Gif, related_name='categories')

    def __str__(self):
        return self.name

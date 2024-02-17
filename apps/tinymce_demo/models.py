from django.conf import settings
from django.db import models
from tinymce.models import HTMLField


# Create your models here.
class TinyMCEPicture(models.Model):
    original = models.ImageField(verbose_name="original", max_length=255)
    converted = models.ImageField(verbose_name="converted", max_length=255)

    def __str__(self):
        return self.original.url + ', ' + self.converted.url


class News(models.Model):
    for iso, _ in settings.LANGUAGES:
        locals()[f"title_{iso}"] = models.CharField(max_length=255, verbose_name=f"title_{iso}")
        locals()[f"description_{iso}"] = HTMLField(max_length=10000, verbose_name=f"description_{iso}")

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'

from django.conf import settings
from django.contrib import admin
from django.utils import translation
from django.utils.safestring import mark_safe

from .models import News, TinyMCEPicture
from .utils import parse_and_download_images


# Register your models here.


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    lang = translation.get_language()
    list_display = 'id', f'title_{lang}', f'description_{lang}'

    def save_model(self, request, obj, form, change):
        if change:
            old_obj = self.model.objects.get(id=obj.id)
            for iso, _ in settings.LANGUAGES:
                description = getattr(old_obj, f"description_{iso}", None)
                if getattr(obj, f"description_{iso}", None) != description:
                    new_desc = parse_and_download_images(getattr(obj, f"description_{iso}", None))
                    setattr(obj, f"description_{iso}", new_desc)
        else:
            for iso, _ in settings.LANGUAGES:
                new_desc = parse_and_download_images(getattr(obj, f"description_{iso}", None))
                setattr(obj, f"description_{iso}", new_desc)
        obj.save()


@admin.register(TinyMCEPicture)
class TinyMCEPictureAdmin(admin.ModelAdmin):
    list_display = 'id', 'original', 'converted', 'get_converted'

    def get_converted(self, obj):
        if obj.converted:
            return mark_safe(f'<img src="{obj.converted.url}" width="150" height="150" />')

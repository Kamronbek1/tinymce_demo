from collections import OrderedDict

from django.conf import settings
from rest_framework import serializers

# from modeltranslation
from .models import News, TinyMCEPicture
from django.utils import translation


class I18nModelSerializer(serializers.ModelSerializer):

    def to_representation(self, instance):
        i18n_fields = getattr(self.Meta, 'i18n_fields', None)
        fields_lang = [f"{field}_{key}" for field in i18n_fields[1] for key, _ in settings.LANGUAGES]
        representation = super().to_representation(instance)
        if i18n_fields[0] == 'catch':
            for k in i18n_fields[1]:
                representation[f'{k}'] = representation.pop("{}_{}".format(k, translation.get_language()))
                if not getattr(instance, "{}_{}".format(k, translation.get_language()), None):
                    for iso, _ in settings.LANGUAGES:
                        if getattr(instance, f'{k}_{iso}', None):
                            representation[f'{k}'] = representation.pop("{}_{}".format(k, iso))
                            break
                        else:
                            continue
                if not representation[k]:
                    representation[k] = None
        return {key: value for key, value in representation.items() if key not in fields_lang}


class NewsSerializer(I18nModelSerializer):
    class Meta:
        model = News
        i18n_fields = ("catch", ('title', 'description'))
        fields = "__all__"


class TinyMCEPictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = TinyMCEPicture
        fields = "__all__"

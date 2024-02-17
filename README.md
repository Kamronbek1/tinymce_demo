# tinymce_demo

## How to use
## 1. Install dependencies from requirements.txt
```commandline
pip install requirements.txt
```
```
Django==4.2.4
django-tinymce==3.6.1
djangorestframework==3.14.0
Pillow==10.0.0
requests==2.31.0
```
## 2. Configuration in settings.py
* add tinymce module name to installed apps
    ```
    INSTALLED_APPS = [
    ....
    ....
    'tinymce',
    ]
    ```
* add media path
    ```
    MEDIA_ROOT = Path(BASE_DIR / 'media')
    MEDIA_URL = '/media/'
    ```
* add tinymce config copy and paste from settings.py
    ```python
    TINYMCE_DEFAULT_CONFIG = {
    ....
    ....
    }
    ```
## 3. Add urls in urls.py
  *
      ```python
      urlpatterns = [
          path('tinymce/', include('tinymce.urls')),
          path('image_upload/', image_upload, name='image_upload'),  # the URL for image upload
      ]
      ```
## 4. Copy and paste utils.py and compresser.py to your project folder

## 5. In admin.py override save_model method
* use parse_and_download_images method 
* method arguments: only html string required

    ```python
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
    ```

-----



MIT License

Copyright (c) 2023 TinymcePicture

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
from datetime import datetime
from pathlib import Path

from PIL import Image
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, views, status
from rest_framework.response import Response

from .utils import make_unique_path_name, compress_img
from .models import News, TinyMCEPicture
from .serializers import NewsSerializer, TinyMCEPictureSerializer


class NewsViewSet(viewsets.ModelViewSet):
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class TinyMCEPictureViewSet(views.APIView):

    def get(self, request):
        param = request.query_params.get("converted")
        param = '/' + '/'.join(param.split('/')[4:])
        print(param)
        data = TinyMCEPicture.objects.get(converted=param)
        serializer = TinyMCEPictureSerializer(data)
        return Response(serializer.data)


@csrf_exempt
def image_upload(request):
    if request.method == 'POST':
        print('tinymce image_upload method called!')
        file = request.FILES['file']  # get the uploaded file
        print(type(file))
        current_datetime = datetime.now().strftime("%Y/%m/%d")

        # Create a directory with the current date and millisecond as the name
        save_path = (Path(settings.MEDIA_ROOT) / Path('uploads') / Path(current_datetime) / file.name)
        save_path = make_unique_path_name(save_path, save_path.suffix)
        save_path.parent.mkdir(parents=True, exist_ok=True)
        print(save_path)
        with open(save_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)

        try:
            Image.open(save_path).verify()
            is_image = True
        except OSError:
            return JsonResponse({'error': 'is not image'})
        if is_image:
            # return a JSON response with the URL of the image
            return JsonResponse({'location': "/" + "/".join(Path(save_path).parts[-6:])})

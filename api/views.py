from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, parsers
from django.conf import settings
from api.utils import process_cv_and_job_description
import os

class UploadCVView(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]  # Для прийому файлів

    def post(self, request):
        file_obj = request.FILES.get('cv')
        if not file_obj:
            return Response({'error': 'No CV file provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Зберегти файл у media/cv.pdf
        file_path = os.path.join(settings.MEDIA_ROOT, 'cv.pdf')
        with open(file_path, 'wb+') as destination:
            for chunk in file_obj.chunks():
                destination.write(chunk)
        
        return Response({'message': 'CV uploaded successfully'}, status=status.HTTP_201_CREATED)


class UploadJobDescriptionView(APIView):
    def post(self, request):
        job_description = request.data.get('job_description')
        if not job_description:
            return Response({'error': 'No job description provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Зберегти в файл
        file_path = os.path.join(settings.MEDIA_ROOT, 'job_description.txt')
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(job_description)
        
        return Response({'message': 'Job description uploaded successfully'}, status=status.HTTP_201_CREATED)


class GetResultView(APIView):
    def get(self, request):
        try:
            result_dict = process_cv_and_job_description()
        except:
            return Response("Missing CV or Job Description", status=status.HTTP_400_BAD_REQUEST)
        
        return Response(result_dict, status=status.HTTP_200_OK)
        

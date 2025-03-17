from django.urls import path
from .views import UploadCVView, UploadJobDescriptionView, GetResultView

urlpatterns = [
    path('upload-cv/', UploadCVView.as_view(), name='upload-cv'),
    path('upload-job-description/', UploadJobDescriptionView.as_view(), name='upload-job-description'),
    path('get-result/', GetResultView.as_view(), name='get-result'),
]

from django.urls import path

from apps.commons.api.tinymce_image_upload_viewset import TinyMCEImagesUploadViewSet

urlpatterns = [
    path('tinymce_image/', TinyMCEImagesUploadViewSet.as_view({'put': 'ImageUpload'}))
]

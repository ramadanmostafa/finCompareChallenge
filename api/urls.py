from django.urls import path
from .views import BulkUploadCsvView

urlpatterns = [
    path('upload/csv/', BulkUploadCsvView.as_view(), name="upload_csv"),
]

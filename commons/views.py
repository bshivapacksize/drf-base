from rest_framework.generics import CreateAPIView
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser

from .serializers import FileSerializer
from .models import FileUpload


class FileView(CreateAPIView):
    parser_classes = [MultiPartParser, FormParser, FileUploadParser]
    serializer_class = FileSerializer
    queryset = FileUpload.objects.all()

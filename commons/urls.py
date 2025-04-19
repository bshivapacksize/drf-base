from django.urls import path

from .views import FileView

urlpatterns = [path("file/", FileView.as_view(), name="file")]

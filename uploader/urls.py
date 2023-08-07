from django.urls import include, path
from .views import *


urlpatterns = [
    path("", index),
    path("submit/", upload_file),
]

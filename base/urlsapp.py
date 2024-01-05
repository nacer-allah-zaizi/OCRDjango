from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('upload_image/',views.upload_image,name='upload_image'),
]

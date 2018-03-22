from django.conf.urls import url
from . import views

urlpatterns = [
    url('v1/api/chhattisgarh', views.index),
]


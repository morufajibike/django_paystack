
from django.conf.urls import include, url

import views

urlpatterns = [
    
    url(r'^start', views.start, name="start"),
   
]

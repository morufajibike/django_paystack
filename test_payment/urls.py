
from django.conf.urls import include, url

import views

urlpatterns = [
    
    url(r'^start', views.start, name="start"),
    #url(r'^result/(?P<reference>.+)/', views.payment_result, name="payment_result"),
    url(r'^result/', views.payment_result, name="payment_result"),

]

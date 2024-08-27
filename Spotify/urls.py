from django.urls import path

from . import views
urlpatterns = [
    path('', views.recommend,name ="dashboard"),
    path('about/',views.prediction,name = "predicty")
    
        
]

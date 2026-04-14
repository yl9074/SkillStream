from django.urls import path
from . import views

# URL 配置 (URLConf)
urlpatterns = [
    path('hello/', views.say_hello)
]
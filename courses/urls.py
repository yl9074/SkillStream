from django.urls import path
from . import views # Import the views from the current folder

# The URL patterns for the courses app
urlpatterns = [
    # When a user visits the root of this app, trigger the course_list view
    path('', views.course_list, name='course_list'), 
    path('<int:course_id>/', views.course_detail, name='course_detail'),
]
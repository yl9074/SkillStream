from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Import the views from the current folder

# The URL patterns for the courses app
urlpatterns = [
    # The URL path remains the same, but it now points to the updated pathway_list view
    path('', views.pathway_list, name='pathway_list'), 
    
    path('catalog/', views.subject_catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('search/', views.search_courses, name='search'),
    path('profile/', views.user_profile, name='user_profile'),
    path('feedback/', views.feedback, name='feedback'),
    path('courses/', views.courses, name='courses'),
    path('<int:pathway_id>/', views.pathway_detail, name='pathway_detail'),
    path('video/<int:video_id>/complete/', views.mark_video_complete, name='mark_video_complete'),
    path('admin-analytics/', views.admin_analytics, name='admin_analytics'),
]
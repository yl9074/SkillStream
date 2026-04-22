from django.urls import path
from django.contrib.auth import views as auth_views
from . import views # Import the views from the current folder

# The URL patterns for the courses app
urlpatterns = [
    # The URL path remains the same, but it now points to the updated pathway_list view
    path('', views.pathway_list, name='pathway_list'), 
    
    # The expected parameter is now pathway_id, pointing to the pathway_detail view
    path('<int:pathway_id>/', views.pathway_detail, name='pathway_detail'),

    path('catalog/', views.subject_catalog, name='catalog'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
from django.urls import path
from . import views # Import the views from the current folder

# The URL patterns for the courses app
urlpatterns = [
    # The URL path remains the same, but it now points to the updated pathway_list view
    path('', views.pathway_list, name='pathway_list'), 
    
    # The expected parameter is now pathway_id, pointing to the pathway_detail view
    path('<int:pathway_id>/', views.pathway_detail, name='pathway_detail'),
]
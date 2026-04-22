from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Subject, Pathway, VideoLesson # 👈 Import the new models here

# 1. Lobby: Display all available learning pathways
def pathway_list(request):
    pathways = Pathway.objects.all()
    return render(request, 'courses/pathway_list.html', {'pathways': pathways})

# 2. Detail Page: Display all video lessons within a specific pathway
def pathway_detail(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    # Retrieve all videos under this pathway, ordered by their sequence number
    videos = pathway.videos.all().order_by('sequence_order') 
    
    context = {
        'pathway': pathway,
        'videos': videos,
    }
    return render(request, 'courses/pathway_detail.html', context)

def subject_catalog(request):
    subjects = Subject.objects.all()
    return render(request, 'courses/subject_catalog.html', {'subjects': subjects})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log the user in after registration
            return redirect('pathway_list')  # Redirect to the pathway list after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

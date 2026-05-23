from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Subject, Pathway, VideoLesson, UserProgress, Quiz, Question, QuizScore # import the new models here

# 1. Lobby: Display all available learning pathways
@login_required
def pathway_list(request):
    pathways = Pathway.objects.all()
    return render(request, 'courses/pathway_list.html', {'pathways': pathways})

# 2. Detail Page: Display all video lessons within a specific pathway
@login_required
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
            return redirect('dashboard')  # redirect to the dashboard after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def take_quiz(request, quiz_id):
    quiz = get_object_or_404(Quiz, id=quiz_id)
    questions = quiz.questions.all()

    if request.method == 'POST':
        correct_answers = 0
        total_questions = questions.count()

        if total_questions > 0:
            for question in questions:
                # get the specific radio button option the user selected for this question
                selected_option = request.POST.get(f'question_{question.id}')
                
                if selected_option == question.correct_answer:
                    correct_answers += 1
            
            score_percentage = (correct_answers / total_questions) * 100
            
            QuizScore.objects.create(
                user=request.user,
                pathway=quiz.pathway,
                score=score_percentage
            )
        
        return redirect('dashboard')

    return render(request, 'courses/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def search_courses(request):
    
    query = request.GET.get('q', '')
    
    if query:
        results = Pathway.objects.filter(title__icontains=query)
    else:
        results = Pathway.objects.none()
        
    context = {
        'results': results,
        'query': query
    }
    
    return render(request, 'courses/search_results.html', context)
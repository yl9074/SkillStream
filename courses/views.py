from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Avg, Count
from django.contrib.auth.decorators import user_passes_test
from .models import Subject, Pathway, VideoLesson, UserProgress, Quiz, Question, QuizScore, UserProfile # import the new models here

# 1. Lobby: Display all available learning pathways
@login_required
def pathway_list(request):
    pathways = Pathway.objects.all()
    return render(request, 'courses/pathway_list.html', {'pathways': pathways})

# 2. Detail Page: Display all video lessons within a specific pathway (WITH TRACKER AND DEBUG)
@login_required
def pathway_detail(request, pathway_id):
    pathway = get_object_or_404(Pathway, id=pathway_id)
    videos = pathway.videos.all().order_by('sequence_order') 
    
    for video in videos:
        UserProgress.objects.get_or_create(
            user=request.user,
            video=video
        )

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
        form.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        form.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        form.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
    return render(request, 'register.html', {'form': form})

@login_required
def dashboard_view(request):
    user = request.user

    videos_watched = UserProgress.objects.filter(user=user, is_completed=True).count()

    score_data = QuizScore.objects.filter(user=user).aggregate(Avg('score'))
    raw_avg = score_data['score__avg']
    avg_score = round(raw_avg, 1) if raw_avg else 0 

    last_progress = UserProgress.objects.filter(user=user).order_by('-completion_date').first()

    context = {
        'videos_watched': videos_watched,
        'avg_score': avg_score,
        'last_progress': last_progress,
    }

    return render(request, 'dashboard.html', context)

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
            
            incorrect_answers = total_questions - correct_answers
            
            QuizScore.objects.create(
                user=request.user,
                pathway=quiz.pathway,
                score=score_percentage
            )
        else:
            score_percentage = 0
            incorrect_answers = 0

        context = {
                'quiz': quiz,
                'score_percentage': round(score_percentage, 1), #rounds to 1 decimal 
                'correct_answers': correct_answers,
                'incorrect_answers': incorrect_answers,
                'total_questions': total_questions
            }
        return render(request, 'courses/quiz_results.html', context)

    return render(request, 'courses/take_quiz.html', {'quiz': quiz, 'questions': questions})

@login_required
def search_courses(request):
    
    query = request.GET.get('q', '').strip()
    
    if query:
        results = Pathway.objects.filter(title__icontains=query) | Pathway.objects.filter(subject__title__icontains=query)
        results = results.distinct()
    else:
        results = Pathway.objects.none()
        
    context = {
        'results': results,
        'query': query
    }
    
    return render(request, 'search_results.html', context)

@login_required
def user_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST' and request.FILES.get('profile_pic'):
        profile.profile_picture = request.FILES['profile_pic']
        profile.save()
        return redirect('user_profile')

    progress_records = UserProgress.objects.filter(user=request.user)
    
    context = {
        'progress_list': progress_records,
        'profile': profile,
    }
    
    return render(request, 'profile.html', context)
    
@login_required
def feedback(request):
    return render(request, 'feedback.html')

@login_required
def courses(request):
    pathways = Pathway.objects.all()
    return render(request, 'courses.html', {'pathways': pathways})

@login_required
def mark_video_complete(request, video_id):
    if request.method == 'POST':
        # Fetch the specific video lesson requested by the user
        video = get_object_or_404(VideoLesson, id=video_id)
        
        # Retrieve the user's progress record, or create a new one if it doesn't exist
        progress, created = UserProgress.objects.get_or_create(user=request.user, video=video)
        
        # Update the completion status to True
        progress.is_completed = True
        progress.save()
        
        # Redirect the user back to the current pathway detail page
        return redirect('pathway_detail', video.pathway.id)

# Security check: Only allow users where is_staff is True
@user_passes_test(lambda u: u.is_staff)
def admin_analytics(request):
    # 1. Total number of registered students (excluding admins)
    total_students = User.objects.filter(is_staff=False).count()

    # 2. Average quiz score across the entire platform
    # The aggregate function returns a dictionary, so we extract the specific value
    avg_score_data = QuizScore.objects.aggregate(Avg('score'))
    average_score = avg_score_data['score__avg'] or 0  # Fallback to 0 if no quizzes taken yet

    # 3. Top 5 Most Popular Videos (Count how many UserProgress records link to each video)
    popular_videos = VideoLesson.objects.annotate(
        view_count=Count('userprogress')
    ).order_by('-view_count')[:5]

    # Pack everything into the context
    context = {
        'total_students': total_students,
        'average_score': round(average_score, 2), # Round to 2 decimal places
        'popular_videos': popular_videos,
    }

    return render(request, 'admin/admin_analytics.html', context)
from django.contrib import admin
from .models import QuizScore, Subject, Pathway, UserProgress, VideoLesson, Quiz, Question

# Register your models here.
admin.site.register(Subject)
admin.site.register(Pathway)
@admin.register(VideoLesson)

class VideoLessonAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('pathway', 'sequence_order', 'youtube_url')
    
    # Add a filter sidebar by Pathway on the right
    list_filter = ('pathway',)
    
    # Default sorting by pathway and sequence order
    ordering = ('pathway', 'sequence_order')


# Quiz Management System Admin

# 1. Use StackedInline to allow questions to be embedded directly within the Quiz creation page
class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1  # Display 1 blank question form by default
    # Organize fields for a cleaner and more intuitive Admin interface
    fields = ('question_text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer')

# 2. Register Quiz (and embed the questions inline)
@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'pathway')  # Display quiz title and associated pathway in the list view
    list_filter = ('pathway',)           # Enable filtering by pathway on the right sidebar
    inlines = [QuestionInline]           # Embed the QuestionInline form here

# 3. Register Question (in case admins want to manage questions individually)
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'quiz', 'correct_answer')
    list_filter = ('quiz',)
    search_fields = ('question_text',)   # Enable search functionality by question text

# 4. Register QuizScore (to easily track students' exam results)
@admin.register(QuizScore)
class QuizScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'pathway', 'score', 'date_taken')
    list_filter = ('pathway', 'date_taken')
    
# 5. Register UserProgress (if not already registered previously)
@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'video', 'is_completed', 'completion_date')
    list_filter = ('is_completed',)
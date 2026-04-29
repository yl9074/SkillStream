from django.contrib import admin
from .models import Subject, Pathway, VideoLesson, Quiz, Question

# Register your models here.
admin.site.register(Subject)
admin.site.register(Pathway)
admin.site.register(Quiz)
admin.site.register(Question)
@admin.register(VideoLesson)
class VideoLessonAdmin(admin.ModelAdmin):
    # Columns to display in the admin list view
    list_display = ('pathway', 'sequence_order', 'youtube_url')
    
    # Add a filter sidebar by Pathway on the right
    list_filter = ('pathway',)
    
    # Default sorting by pathway and sequence order
    ordering = ('pathway', 'sequence_order')
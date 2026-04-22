from django.contrib import admin
from .models import Subject, Pathway, VideoLesson, Quiz, Question

# Register your models here.
admin.site.register(Subject)
admin.site.register(Pathway)
admin.site.register(VideoLesson)
admin.site.register(Quiz)
admin.site.register(Question)
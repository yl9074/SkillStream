from django.db import models
from django.contrib.auth.models import User # Import Django's built-in User model

# 1. Subject (The main category/discipline)
class Subject(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()

    def __str__(self):
        return self.title

# 2. Pathway (A specific learning path within a subject)
class Pathway(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='pathways')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.subject.title} - {self.title}"

# 3. Video Lesson (Individual video modules in a pathway)
class VideoLesson(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='videos')
    youtube_url = models.CharField(max_length=500)
    sequence_order = models.IntegerField()

    def __str__(self):
        return f"Video {self.sequence_order} in {self.pathway.title}"

# 4. Quiz (An assessment linked to a specific pathway)
class Quiz(models.Model):
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE, related_name='quizzes')
    title = models.CharField(max_length=200)

    def __str__(self):
        return f"Quiz: {self.title}"

# 5. Question (Individual questions belonging to a quiz, including multiple-choice options)
class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=200, blank=True, null=True)
    option_b = models.CharField(max_length=200, blank=True, null=True)
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)
    correct_answer = models.CharField(max_length=200) # Stores the text of the correct answer

    def __str__(self):
        return self.question_text
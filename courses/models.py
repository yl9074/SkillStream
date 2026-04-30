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
    
    def get_embed_url(self):
        """Automatically convert various YouTube URLs to embeddable iframe URLs."""
        # 1. Clean up any leading/trailing whitespace or newlines
        url = self.youtube_url.strip()
        
        # 🛑 Defensive handling: Case 3 - If the user pasted the entire raw <iframe> HTML
        if "<iframe" in url and 'src="' in url:
            # Extract exactly the URL: split by 'src="' to get the second half, 
            # then split by the closing '"' to grab the first part.
            extracted_url = url.split('src="')[1].split('"')[0]
            return extracted_url
            
        # Case 1: Standard long YouTube URL (contains watch?v=)
        if "watch?v=" in url:
            video_id = url.split("watch?v=")[1].split("&")[0]
            return f"https://www.youtube.com/embed/{video_id}"
            
        # Case 2: Shortened share URL (contains youtu.be/)
        elif "youtu.be/" in url:
            video_id = url.split("youtu.be/")[1].split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
            
        # Case 4: Already a valid embed URL (or unrecognized format), return as-is
        return url

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
    
class UserProgress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(VideoLesson, on_delete=models.CASCADE)
    is_completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    class Meta:
        # A user can only have one progress record per video
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user.username} - {self.video.title} - {'Done' if self.is_completed else 'Pending'}"
    
class QuizScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pathway = models.ForeignKey(Pathway, on_delete=models.CASCADE)
    score = models.DecimalField(max_digits=5, decimal_places=2) # Example: 85.50
    date_taken = models.DateTimeField(auto_now_add=True)

    class Meta:
        # A user can take a quiz multiple times
        ordering = ['-date_taken'] 

    def __str__(self):
        return f"{self.user.username} - {self.pathway.title} - {self.score}%"
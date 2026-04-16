from django.db import models
from django.contrib.auth.models import User # Use Django's built-in User model for instructors

# 1. Category Table (e.g., Programming, Design, Marketing)
class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name="Category Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")

    class Meta:
        verbose_name_plural = "Categories" # Correct the plural name in Admin

    def __str__(self):
        return self.name

# 2. Main Course Table
class Course(models.Model):
    title = models.CharField(max_length=200, verbose_name="Course Title")
    # ForeignKey: one category can have multiple courses
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Category")
    # Instructor: linked to Django's built-in User model
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Instructor")
    description = models.TextField(verbose_name="Course Description")
    is_published = models.BooleanField(default=False, verbose_name="Is Published")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return self.title

# 3. Lesson Table (Specific chapters within a course)
class Lesson(models.Model):
    # on_delete=models.CASCADE: if the course is deleted, its lessons are also deleted
    # related_name='lessons': allows access via course.lessons.all()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons', verbose_name="Course")
    title = models.CharField(max_length=200, verbose_name="Lesson Title")
    content = models.TextField(blank=True, null=True, verbose_name="Content")
    video_url = models.URLField(blank=True, null=True, verbose_name="Video URL")
    order = models.IntegerField(default=0, verbose_name="Order")

    class Meta:
        # Sort by the 'order' field in ascending order
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"
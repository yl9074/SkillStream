from django import template
from courses.models import QuizScore, UserProgress

register = template.Library()

@register.simple_tag
def get_chart_data():
    
    passed_count = QuizScore.objects.filter(score__gte=50).count()
    
    failed_count = QuizScore.objects.filter(score__lt=50).count()
    
    in_progress_count = UserProgress.objects.filter(is_completed=False).count()
    
    return f"[{passed_count}, {failed_count}, {in_progress_count}]"
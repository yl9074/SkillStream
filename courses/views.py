from django.shortcuts import render, get_object_or_404
from .models import Course # Import the Course model (our database table)

# Create your views here.
def course_list(request):
    # 1. Fetch all published courses from the database
    published_courses = Course.objects.filter(is_published=True)
    
    # 2. Pack the data into a dictionary called 'context' (our serving tray)
    context = {
        'courses': published_courses
    }
    
    # 3. Pass the context to the HTML template for rendering
    return render(request, 'courses/course_list.html', context)

def course_detail(request, course_id):
    # 1. 根据客人的要求（course_id），去仓库找那门特定的课。如果找不到，就报 404 错误。
    course = get_object_or_404(Course, id=course_id)
    
    # 2. 顺便把这门课下面所有的视频（Lessons）也拿出来，按照之前定的 order 排好队
    lessons = course.lessons.all() 
    
    # 3. 装盘
    context = {
        'course': course,
        'lessons': lessons
    }
    
    # 4. 递给专用的详情页模板
    return render(request, 'courses/course_detail.html', context)
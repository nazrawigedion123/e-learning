from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from ..models import Lesson,Course

from django.utils import timezone
@login_required
@require_POST
def complete_lesson(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    progress = lesson.get_user_progress(request.user)
    progress.completed = True
    progress.completed_at = timezone.now()
    progress.save()
    return JsonResponse({'status': 'success'})


@login_required
def get_course_progress(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    progress = course.get_user_progress(request.user)

    data = {
        'course': {
            'completion': progress.completion_percentage,
            'status': progress.status,
        },
        'chapters': [],
    }

    for chapter in course.chapters.all():
        chapter_progress = chapter.get_user_progress(request.user)
        data['chapters'].append({
            'id': chapter.id,
            'title': chapter.title,
            'completed': chapter_progress.completed,
            'lessons': [
                {
                    'id': lesson.id,
                    'title': lesson.title,
                    'completed': lesson.get_user_progress(request.user).completed,
                    'quiz_attempts': lesson.quiz.get_user_attempts(request.user).count() if hasattr(lesson,
                                                                                                    'quiz') else 0
                }
                for lesson in chapter.lessons.all()
            ]
        })

    return JsonResponse(data)
from rest_framework import viewsets, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from ..models import Course, Chapter, Lesson, Quiz, Question, Option, Progress
from ..serializers import CourseSerializers, ChapterSerializers, LessonSerializers, QuizSerializers, QuestionSerializers, \
    OptionSerializers, ProgressSerializers


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chapters(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is enrolled in the course
    if request.user not in course.users.all():
        return Response({"error": "You are not enrolled in this course"}, status=status.HTTP_403_FORBIDDEN)

    chapters = course.chapters.all()
    serializer = ChapterSerializers(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_chapter(request, pk, chapter_pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    # Check if the user is enrolled in the course
    if request.user not in course.users.all():
        return Response({"error": "You are not enrolled in this course"}, status=status.HTTP_403_FORBIDDEN)

    try:
        chapter = course.chapters.get(pk=chapter_pk)  # Corrected access to chapters
    except Chapter.DoesNotExist:
        return Response({"error": "Chapter not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = ChapterSerializers(chapter, many=False)
    return Response(serializer.data)
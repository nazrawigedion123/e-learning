from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from tutorial.quickstart.serializers import UserSerializer

from ..models import Course, Chapter
from ..serializers import ChapterSerializers,CourseSerializers
from user.permission import IsAdminOrInstructorOwner,IsClient




@api_view(['GET'])
@permission_classes([IsClient])
def get_chapters(request, pk):
    """
    Retrieve all chapters for a specific course.
    Only authenticated users enrolled in the course can access this endpoint.
    """
    course = get_object_or_404(Course, pk=pk)
    if not (request.user in course.users.all() or request.user == course.instructor or request.user.is_staff):
        return Response({"error": "You are not enrolled in this course and are not the instructor or an admin"},
                        status=status.HTTP_403_FORBIDDEN)




    chapters = course.chapters.all()
    serializer = ChapterSerializers(chapters, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsClient])
def get_chapter(request, pk, chapter_pk):
    """
    Retrieve a specific chapter for a course.
    Only authenticated users enrolled in the course can access this endpoint.
    """
    course = get_object_or_404(Course, pk=pk)

    if not (request.user in course.users.all() or request.user == course.instructor or request.user.is_staff):
        return Response({"error": "You are not enrolled in this course "},
                        status=status.HTTP_403_FORBIDDEN)

    chapter = get_object_or_404(Chapter, pk=chapter_pk, course=course)
    serializer = ChapterSerializers(chapter, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminOrInstructorOwner])
def create_chapter(request, pk):
    course = get_object_or_404(Course, pk=pk)
    data = request.data.copy()
    data['course'] = course.pk  # Explicitly include the course ID

    serializer = ChapterSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminOrInstructorOwner])
def update_chapter(request, pk, chapter_pk):
    """
    Update a specific chapter for a course.
    Only admins or the instructor who owns the course can update a chapter.
    """
    course = get_object_or_404(Course, pk=pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk, course=course)
    serializer = ChapterSerializers(chapter, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminOrInstructorOwner])
def delete_chapter(request, chapter_pk):
    """
    Delete a specific chapter.
    Only admins or the instructor who owns the course can delete a chapter.
    """
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    chapter.delete()
    return Response({"message": "Chapter was successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
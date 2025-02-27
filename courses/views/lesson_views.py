
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from ..models import Chapter,Lesson
from ..serializers import  LessonSerializers
from user.permission import IsAdminOrInstructorOwner, IsClient



@api_view(['GET'])
@permission_classes([IsClient])
def get_lesson(request, pk,chapter_pk,lesson_pk):
    lesson = get_object_or_404(Lesson, pk=lesson_pk)
    serializer = LessonSerializers(lesson, many=False)
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAdminOrInstructorOwner])
def create_lesson(request, pk,chapter_pk):
    chapter=get_object_or_404(Chapter,pk=chapter_pk)
    data= {'chapter': chapter.pk,
           'title': 'Sample title',
           'description':'Sample description',
           }

    serializer=LessonSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['PUT'])
@permission_classes([IsAdminOrInstructorOwner])
def update_lesson(request, pk,chapter_pk,lesson_pk):
    lesson=get_object_or_404(Lesson,pk=lesson_pk)
    data= request.data
    serializer=LessonSerializers(lesson,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminOrInstructorOwner])
def delete_lesson(request,pk,lesson_pk):
    lesson=get_object_or_404(Lesson,pk=lesson_pk)
    lesson.delete()
    return Response({'message':"lesson was deleted"},status=status.HTTP_204_NO_CONTENT)






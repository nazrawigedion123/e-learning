from django.core.serializers import serialize
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Lesson, Course,Quiz
from backend.user.permission import IsClient, IsAdminOrInstructorOwner
from ..serializers import QuizSerializers



@api_view(['GET'])
@permission_classes([IsClient])
def get_quiz(request,pk,chapter_pk,lesson_pk,quiz_pk):
    """
    Get a specific quiz
    """
    course = get_object_or_404(Course, pk=pk)
    if request.user not in course.users.all() and request.user != course.instructor and not request.user.is_staff:
        return Response({"response":"You are not enrolled in this course"},status=status.HTTP_403_FORBIDDEN)
    quiz=get_object_or_404(Quiz,pk=quiz_pk)
    serializer= QuizSerializers(quiz,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminOrInstructorOwner])
def create_quiz(request,pk,chapter_pk,lesson_pk):
    data=request.data.copy()
    data['lesson']=lesson_pk
    serializer=QuizSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminOrInstructorOwner])
def update_quiz(request, pk,chapter_pk,lesson_pk,quiz_pk):
    quiz=get_object_or_404(Quiz,pk=quiz_pk)
    data=request.data
    serializer=QuizSerializers(quiz,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminOrInstructorOwner])
def delete_quiz(request,pk,chapter_pk,lesson_pk,quiz_pk):
    quiz=get_object_or_404(Quiz,pk=quiz_pk)
    quiz.delete()
    return Response({"message":"quiz was deleted"},status=status.HTTP_204_NO_CONTENT)






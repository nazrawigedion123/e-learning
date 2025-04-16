from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Question,Quiz,Course,Option
from user.permission import IsClient,IsAdminOrInstructorOwner
from ..serializers import QuestionSerializers,OptionSerializers


@api_view(['GET'])
@permission_classes([IsClient])
def get_question(request,pk,chapter_pk,lesson_pk,quiz_pk,question_pk):
    """
    Get a specific quiz
    """
    course = get_object_or_404(Course, pk=pk)
    if not (request.user in course.users.all() or request.user == course.instructor or request.user.is_staff):
        return Response({"error": "You are not enrolled in this course "},
                        status=status.HTTP_403_FORBIDDEN)
    question=get_object_or_404(Question,pk=question_pk)
    serializer= QuestionSerializers(question,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminOrInstructorOwner])
def create_question(request,pk,chapter_pk,lesson_pk,quiz_pk):
    data=request.data.copy()
    data['quiz']=quiz_pk
    serializer=QuestionSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAdminOrInstructorOwner])
def update_question(request, pk,chapter_pk,lesson_pk,quiz_pk,question_pk):
    question=get_object_or_404(Question,pk=question_pk)
    data=request.data
    serializer=QuestionSerializers(question,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@permission_classes([IsAdminOrInstructorOwner])
def delete_question(request,pk,chapter_pk,lesson_pk,quiz_pk,question_pk):
    question=get_object_or_404(Question,pk=question_pk)
    question.delete()
    return Response({"message":"question was deleted"},status=status.HTTP_204_NO_CONTENT)

#create option
@api_view(['POST'])
@permission_classes([IsAdminOrInstructorOwner])
def create_option(request,pk,chapter_pk,lesson_pk,quiz_pk,question_pk):
    data=request.data.copy()
    data['question']=question_pk
    serializer=OptionSerializers(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_201_CREATED)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#edit option
@api_view(['PUT'])
@permission_classes([IsAdminOrInstructorOwner])
def update_option(request, pk,chapter_pk,lesson_pk,quiz_pk,question_pk,option_pk):
    option=get_object_or_404(Option,pk=option_pk)
    data=request.data
    serializer=OptionSerializers(option,data=data,partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#delete option
@api_view(['DELETE'])
@permission_classes([IsAdminOrInstructorOwner])
def delete_option(request,pk,chapter_pk,lesson_pk,quiz_pk,question_pk,option_pk):
    option=get_object_or_404(Option,pk=option_pk)
    option.delete()
    return Response({"message":"option was deleted"},status=status.HTTP_204_NO_CONTENT)

from django.core.serializers import serialize
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Course,Chapter,Lesson,Quiz,Question,Option,Progress
from .serializers import CourseSerializers,ChapterSerializers,LessonSerializers,QuizSerializers,QuestionSerializers,OptionSerializers,ProgressSerializers

# Create your views here.

@api_view(['GET'])
def get_courses(request):
    courses=Course.objects.all()
    serializer=CourseSerializers(courses,many=True)
    return (Response(serializer.data))
@api_view(['GET'])
def get_course(request,pk):
    try:
        course=Course.object.get(pk=pk)
    except Course.DoesNotExist:
        course=None
    serializer=CourseSerializers(course,many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAdminUser])
def create_course(request):
    data=request.data
    course=Course.objects.create(
        title= data['title'],
        description=data['description']

    )
    serializer=CourseSerializers(course,many=False)
    return Response(serializer.data)





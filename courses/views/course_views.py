
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Course
from ..serializers import CourseSerializers
from user.permission import IsAdminOrInstructorOwner


# Create your views here.

@api_view(['GET'])
def get_courses(request):
    courses = Course.objects.all()
    serializer = CourseSerializers(courses, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = CourseSerializers(course, many=False, context={'request': request})
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminOrInstructorOwner])
def create_course(request):
    data = request.data
    course = Course.objects.create(
        title=data['title'],
        description=data['description'],
        instructor=request.user

    )
    serializer = CourseSerializers(course, many=False)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAdminOrInstructorOwner])
def update_course(request,pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "course not found"}, status=status.HTTP_404_NOT_FOUND)
    data=request.data


    if data['title']:
        course.title=data['title']
    if data['description']:
        course.description=data['description']
    course.save()

    serializer= CourseSerializers(course,many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAdminOrInstructorOwner])
def delete_course(request, pk):
    """
    Delete a course by ID.
    Only admins or the instructor who owns the course can delete it.
    """
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response(
            {"error": "Course not found"},
            status=status.HTTP_404_NOT_FOUND
        )

    # Check if the user has permission to delete the course
    # This is handled by the `IsAdminOrInstructorOwner` permission class,
    # but you can add additional checks here if needed.

    course.delete()
    return Response(
        {"message": "Course was successfully deleted"},
        status=status.HTTP_204_NO_CONTENT
    )


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def enroll_course(request, pk):
    try:
        course = Course.objects.get(pk=pk)
    except Course.DoesNotExist:
        return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user in course.users.all():
        return Response({"error": "User already enrolled in this course"}, status=status.HTTP_400_BAD_REQUEST)

    course.users.add(user)
    course.save()

    return Response({"message": "Successfully enrolled in the course"}, status=status.HTTP_200_OK)








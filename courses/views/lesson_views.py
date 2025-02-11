from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from ..models import Course, Chapter
from ..serializers import ChapterSerializers, LessonSerializers
from user.permission import IsAdminOrInstructorOwner, IsClient
from ..models import Lesson,Chapter

@api_view(['GET'])
@permission_classes([IsClient])
def get

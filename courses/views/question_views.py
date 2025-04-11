from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Question,Quiz,Course
from user.permission import IsClient,IsAdminOrInstructorOwner


# @api_view(['POST'])
# @permission_classes([IsAdminOrInstructorOwner])
# def create_question(request,pk,chapter_pk,lesson_pk,)
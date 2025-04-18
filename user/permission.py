from rest_framework import permissions
from rest_framework.permissions import BasePermission


class IsAdminOrInstructorOwner(permissions.BasePermission):
    """
    Custom permission to allow only admin users or the instructor who created the course
    to perform actions like update or delete.
    """

    def has_object_permission(self, request, view, obj):
        # Admin users have full permissions
        if request.user.role == 'admin':
            return True

        # Instructors can only modify their own courses
        if request.user.role == 'instructor' and obj.instructor == request.user:
            return True

        # Deny by default
        return False
class IsClient(permissions.BasePermission):
    """
    Custom permission to allow only admin users or the instructor who created the course
    to perform actions like update or delete.
    """

    def has_object_permission(self, request, view, obj):
        # Admin users have full permissions
        if request.user.role == 'admin':
            return True

        # Instructors can only modify their own courses
        if request.user.role == 'instructor' and obj.instructor == request.user:
            return True
        if request.user.role == 'client':
            return True

        # Deny by default
        return False


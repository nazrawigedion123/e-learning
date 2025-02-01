from . import views
from django.urls import path

urlpatterns=[
    path('',views.get_courses,name="courses_view"),
    path('<int:pk>/',views.get_course,name="course_view"),
    path('create/',views.create_course,name="create_course_view"),
]
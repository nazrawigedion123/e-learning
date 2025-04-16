from django.urls import path

from ..views import progress_views as views


urlpatterns=[
   path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/complete_lesson/", views.complete_lesson, name="complete_lesson"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/get_course_progress/", views.get_course_progress, name="get_course_progress"),

]
from ..views import lesson_views as views
from django.urls import path

urlpatterns=[
    path("<int:pk>/chapter/<int:chapter_pk/lesson/<int:lesson_pk/",views.get_lesson,name="get_lesson"),
    path("<int:pk>chapter/<int:chapter_pk>/create/",views.create_lesson,name="create_lesson"),
    path("<int:pk>chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/update/",views.update_lesson,name="update_lesson"),
    path("<int:pk>chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/delete/",views.delete_lesson,name="delete_lesson"),

]
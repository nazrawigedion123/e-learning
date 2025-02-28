from django.urls import path
from ..views import quiz_views as views
urlpatterns=[
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/",views.get_quiz,name="get_quiz"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/create/",views.create_quiz,name="create_quiz"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/update/",views.update_quiz,name="update_quiz"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/delete/",views.delete_quiz,name="delete_quiz"),
]
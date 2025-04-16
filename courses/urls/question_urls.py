from django.urls import path
from ..views import question_views as views
urlpatterns=[
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/",views.get_question,name="get_question"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/create/",views.create_question,name="create_question"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/update/",views.update_question,name="update_question"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/delete/",views.delete_question,name="delete_question"),
    #option urls
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/create/",views.create_option,name="create_option"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/option/<int:option_pk>/update/",views.update_option,name="update_option"),
    path("<int:pk>/chapter/<int:chapter_pk>/lesson/<int:lesson_pk>/quiz/<int:quiz_pk>/question/<int:question_pk>/option/<int:option_pk>/delete/",views.delete_option,name="delete_option"),
]
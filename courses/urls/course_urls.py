from ..views import course_views as views
from django.urls import path

urlpatterns=[
    path('',views.get_courses,name="courses_view"),
    path('<int:pk>/',views.get_course,name="course_view"),
    path('create/',views.create_course,name="create_course_view"),
    path('update/<int:pk>/', views.update_course, name='update_course'),
    path('delete/<int:pk>/', views.delete_course, name='delete_course'),
    path('enroll/<int:pk>/', views.enroll_course, name='enroll_course'),
]

from ..views import chapter_views as views
from django.urls import path

urlpatterns=[
    path('<int:pk>/chapters/',views.get_chapters,name="chapters_view"),

    path('<int:pk>/chapter/<int:chapter_pk>/',views.get_chapter,name="chapter_view"),
    path('<int:pk>/chapter/create/',views.create_chapter,name="create_chapter_view"),
    path('<int:pk>/chapter/update/<int:chapter_pk>/', views.update_chapter, name='update_chapter'),
    path('delete/chapter/<int:chapter_pk>/', views.delete_chapter, name='delete_chapter'),
]

from ..views import chapter_views as views
from django.urls import path

urlpatterns=[
    path('<int:pk>/',views.get_chapters,name="chapters_view"),
    path('<int:pk>/<int:chapter_pk>/',views.get_chapter,name="chapter_view"),
    path('<int:pk>/create/',views.create_chapter,name="create_chapter_view"),
    path('<int:pk>/update/<int:chapter_pk>/', views.update_chapter, name='update_chapter'),
    path('delete/<int:chapter_pk>/', views.delete_chapter, name='delete_chapter'),
]

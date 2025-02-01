from django.contrib import admin
from .models import Course,Chapter,Lesson,Quiz,Question,Option,Progress


# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Progress)
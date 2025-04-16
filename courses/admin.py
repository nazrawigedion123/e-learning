from django.contrib import admin
from .models import (Course,Chapter,Lesson,Quiz,Question,Option,Progress,
                     ChapterProgress, LessonProgress, QuizAttempt)


# Register your models here.
admin.site.register(Course)
admin.site.register(Chapter)
admin.site.register(Lesson)
admin.site.register(Quiz)
admin.site.register(Question)
admin.site.register(Option)


class ChapterProgressInline(admin.TabularInline):
    model = ChapterProgress
    extra = 0

class LessonProgressInline(admin.TabularInline):
    model = LessonProgress
    extra = 0

class QuizAttemptInline(admin.TabularInline):
    model = QuizAttempt
    extra = 0

@admin.register(Progress)
class ProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'completion_percentage', 'status')
    list_filter = ('status', 'course')
    inlines = [ChapterProgressInline, LessonProgressInline, QuizAttemptInline]
    readonly_fields = ('completion_percentage',)
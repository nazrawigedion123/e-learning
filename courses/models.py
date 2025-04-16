from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
from django.core.exceptions import ValidationError

from datetime import timedelta

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    description= models.TextField(blank=True,null=True)
    users= models.ManyToManyField(User, blank=True, )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')  # Add this field

    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_progress(self, user):
        return Progress.objects.get_or_create(user=user, course=self)[0]

    def __str__(self):
        return self.title

class Chapter(models.Model):
    course=models.ForeignKey(Course,related_name='chapters', on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    description= models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_progress(self, user):
        progress = Progress.objects.get(user=user, course=self.course)
        return ChapterProgress.objects.get_or_create(
            progress=progress,
            chapter=self
        )[0]

    def __str__(self):
        return self.title

class Lesson(models.Model):
    chapter=models.ForeignKey(Chapter,related_name='lessons',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    description= models.TextField(null=True,blank=True)
    video=models.FileField(upload_to='video/', default='video/examples.mp4',blank=True,null=True)
    pdf=models.FileField(upload_to='pdf/',blank=True,null=True)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_progress(self, user):
        progress = Progress.objects.get(user=user, course=self.chapter.course)
        return LessonProgress.objects.get_or_create(
            progress=progress,
            lesson=self
        )[0]

    def __str__(self):
        return self.title
class Quiz(models.Model):
    lesson=models.ForeignKey(Lesson,related_name='quiz',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_user_attempts(self, user):
        progress = Progress.objects.get(user=user, course=self.lesson.chapter.course)
        return QuizAttempt.objects.filter(progress=progress, quiz=self).order_by('-attempt_number')

    def __str__(self):
        return self.title
class Question(models.Model):
    quiz=models.ForeignKey(Quiz,related_name='questions',on_delete=models.CASCADE)
    question=models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question
class Option(models.Model):
    question=models.ForeignKey(Question,related_name='options',on_delete=models.CASCADE)
    option=models.TextField()
    is_answer=models.BooleanField(default=False)

    def __str__(self):
        return self.option


class Progress(models.Model):
    class Status(models.TextChoices):
        NOT_STARTED = 'not_started', 'Not Started'
        IN_PROGRESS = 'in_progress', 'In Progress'
        COMPLETED = 'completed', 'Completed'

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='user_progress')
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED)
    last_accessed = models.DateTimeField(auto_now=True)

    # Chapter-level tracking
    completed_chapters = models.ManyToManyField(Chapter, blank=True, through='ChapterProgress')

    # Lesson-level tracking
    completed_lessons = models.ManyToManyField(Lesson, blank=True, through='LessonProgress')

    # Quiz-level tracking
    quiz_attempts = models.ManyToManyField(Quiz, blank=True, through='QuizAttempt')

    class Meta:
        unique_together = ('user', 'course')
        indexes = [
            models.Index(fields=['user', 'course']),
        ]

    @property
    def completion_percentage(self):
        total_lessons = Lesson.objects.filter(chapter__course=self.course).count()
        if total_lessons == 0:
            return 0
        return round((self.completed_lessons.filter(lessonprogress__completed=True).count() / total_lessons) * 100, 2)

    def update_status(self):
        if self.completion_percentage == 100:
            self.status = self.Status.COMPLETED
        elif self.completion_percentage > 0:
            self.status = self.Status.IN_PROGRESS
        else:
            self.status = self.Status.NOT_STARTED
        self.save()
    def __str__(self):
        return f"{self.user.username} - {self.course.title} Progress"


class ChapterProgress(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('progress', 'chapter')


class LessonProgress(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(default=timedelta())
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('progress', 'lesson')


class QuizAttempt(models.Model):
    progress = models.ForeignKey(Progress, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    attempt_number = models.PositiveIntegerField(default=1)
    score = models.DecimalField(max_digits=5, decimal_places=2)
    passed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(auto_now_add=True)
    answers = models.JSONField(default=dict)  # Stores user's answers

    class Meta:
        unique_together = ('progress', 'quiz', 'attempt_number')
        ordering = ['-attempt_number']

"""
Implementation Summary:

    Granular Tracking:

        Course-level: Overall completion percentage and status

        Chapter-level: Track which chapters are completed

        Lesson-level: Track completion and time spent

        Quiz-level: Track attempts, scores, and answers

    Automatic Updates:

        Signals automatically update chapter completion when lessons are completed

        Course status updates when chapters are completed

    Easy Access:

        Added utility methods to each model to get user-specific progress

        Comprehensive JSON API endpoint to get all progress data

    Admin Interface:

        View all progress data in one place

        See relationships between course, chapters, lessons, and quizzes

To use this system:

    Call complete_lesson when a user finishes a lesson

    Use get_course_progress to display progress to users

    Quiz attempts should create QuizAttempt records with scores"""





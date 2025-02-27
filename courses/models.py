from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class Course(models.Model):
    title = models.CharField(max_length=200)
    description= models.TextField(blank=True,null=True)
    users= models.ManyToManyField(User, blank=True, )
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    instructor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_courses')  # Add this field

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    course=models.ForeignKey(Course,related_name='chapters', on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    description= models.TextField(blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)

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

    def __str__(self):
        return self.title
class Quiz(models.Model):
    lesson=models.ForeignKey(Lesson,related_name='quiz',on_delete=models.CASCADE)
    title=models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

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
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course,related_name='progresses', on_delete=models.CASCADE)
    completed_lessons = models.ManyToManyField(Lesson, blank=True)
    quiz_scores = models.JSONField(default=dict)  # Store scores as a dictionary {quiz_id: score}
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} Progress"


from rest_framework import serializers
from .models import Course, Chapter, Lesson, Quiz, Question, Option, Progress

class OptionSerializers(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = '__all__'

class QuestionSerializers(serializers.ModelSerializer):
    options = OptionSerializers(many=True, read_only=True,)

    class Meta:
        model = Question
        fields = '__all__'

class QuizSerializers(serializers.ModelSerializer):
    questions = QuestionSerializers(many=True, read_only=True,)

    class Meta:
        model = Quiz
        fields = '__all__'

class LessonSerializers(serializers.ModelSerializer):
    quiz = serializers.SerializerMethodField()

    class Meta:
        model = Lesson
        fields = '__all__'

    def get_quiz(self, obj):
        quiz = obj.quiz.first()
        return QuizSerializers(quiz).data if quiz else None

class ChapterSerializers(serializers.ModelSerializer):
    lessons = LessonSerializers(many=True, read_only=True, )

    class Meta:
        model = Chapter
        fields = '__all__'



class CourseSerializers(serializers.ModelSerializer):
    chapters = ChapterSerializers(many=True, read_only=True, )
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_is_enrolled(self, obj):
        # Ensure the request object is available in the context
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return request.user in obj.users.all()
        return False


class ProgressSerializers(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    course = serializers.PrimaryKeyRelatedField(read_only=True)
    completed_lessons = LessonSerializers(many=True, read_only=True)

    class Meta:
        model = Progress
        fields = '__all__'

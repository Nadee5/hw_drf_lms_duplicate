from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    count_lessons = SerializerMethodField()
    lesson = LessonSerializer(many=True, read_only=True)

    def get_count_lessons(self, obj):
        return obj.lesson.all().count()

    class Meta:
        model = Course
        fields = ['title', 'description', 'preview', 'count_lessons', 'lesson']

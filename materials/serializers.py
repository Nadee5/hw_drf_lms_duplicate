from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson
from materials.validators import validator_url


class LessonSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для модели урока"""
    url = serializers.URLField(validators=[validator_url])

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


class CourseDetailSerializer(serializers.ModelSerializer):
    """Сериализатор просмотра информации о курсе, включает в себя
       поля количества уроков, списка уроков этого курса и признак
       подписки текущего пользователя на этот курс (bool)"""
    lessons_count = SerializerMethodField()
    lessons_list = SerializerMethodField()
    is_subscribed = SerializerMethodField()

    def user_(self):
        """Получаем текущего пользователя"""
        request = self.context.get('request', None)
        if request:
            return request.user
        return None

    def get_is_subscribed(self, course):
        """Проверяем, есть ли в наборе подписок курса объект с текущим пользователем"""
        return course.subscription_set.filter(user=self.user_()).exists()

    @staticmethod
    def get_lessons_count(course):
        """Получаем количество уроков для данного курса"""
        return Lesson.objects.filter(course=course).count()

    @staticmethod
    def get_lessons_list(course):
        """Получаем список уроков для данного курса"""
        return LessonSerializer(Lesson.objects.filter(course=course), many=True).data

    class Meta:
        model = Course
        fields = '__all__'

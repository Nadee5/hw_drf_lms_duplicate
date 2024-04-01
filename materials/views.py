from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from materials.models import Course, Lesson
from materials.paginators import MaterialsPaginator
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer, CourseDetailSerializer


class CourseViewSet(viewsets.ModelViewSet):
    default_serializer = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = MaterialsPaginator
    serializers_choice = {
        'retrieve': CourseDetailSerializer,
    }

    def get_serializer_class(self):
        """Определяем сериализатор с учетом запрашиваемого действия
        (self.action = list, retrieve, create, update,delete).
        Если действие не указано в словарике serializers_choice - используется default_serializer"""
        return self.serializers_choice.get(self.action, self.default_serializer)

    def get_permissions(self):
        """Определяем права доступа с учетом запрашиваемого действия"""
        if self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action in ['retrieve', 'update']:
            self.permission_classes = [IsModerator | IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]

        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]
    # permission_classes = [AllowAny]

    def perform_create(self, serializer):
        """Привязываем текущего пользователя к создаваемому объекту"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = MaterialsPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator | IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]

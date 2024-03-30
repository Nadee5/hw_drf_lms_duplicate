from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from materials.models import Course, Lesson
from materials.permissions import IsModerator, IsOwner
from materials.serializers import CourseSerializer, LessonSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()

    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = [~IsModerator]
        elif self.action == 'retrieve':
            self.permission_classes = [IsModerator, IsOwner]
        elif self.action == 'update':
            self.permission_classes = [IsModerator, IsOwner]
        elif self.action == 'partial_update':
            self.permission_classes = [IsModerator, IsOwner]
        elif self.action == 'destroy':
            self.permission_classes = [IsOwner]

        return [permission() for permission in self.permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonSerializer
    permission_classes = [~IsModerator]


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator, IsOwner]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsModerator, IsOwner]


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from materials.models import Course
from users.models import User, Payment, Subscription
from users.serializers import UserSerializer, PaymentSerializer, UserRetrieveSerializer, SubscriptionSerializer


class UserCreateAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        """Переопределение метода для сохранения хешированного пароля в бд
        (если пароль не хешируется - пользователь не считается активным
        и токен авторизации не создается)"""
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        password = serializer.data["password"]
        user = User.objects.get(pk=serializer.data["id"])
        user.set_password(password)
        user.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class UserRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = UserRetrieveSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserDestroyAPIView(generics.DestroyAPIView):
    queryset = User.objects.all()


class UserListAPIView(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class PaymentListAPIView(generics.ListAPIView):
    """Просмотр списка платежей с фильтрацией по курсу, уроку и способу оплаты,
       и с сортировкой по дате(по умолчанию в модели сортировка по убыванию, при запросе можно изменить с помощью -)"""
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method',)
    ordering_fields = ('payment_date',)


class SubscriptionAPIView(APIView):
    """Контроллер управления подпиской пользователя на курс.
       В запросе передаем id курса, и если подписка на данный курс у текущего пользователя
       существует - удаляем, если нет - создаем"""

    serializer_class = SubscriptionSerializer

    @staticmethod
    def post(request, pk):
        queryset = Course.objects.filter(pk=pk)
        user = request.user
        course = get_object_or_404(queryset=queryset)
        sub_item = Subscription.objects.filter(course=course, user=user)

        if sub_item.exists():
            sub_item.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(user=user, course=course)
            message = 'Подписка добавлена'
        return Response({'message': message})

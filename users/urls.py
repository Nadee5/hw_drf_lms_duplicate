from django.urls import path

from users.apps import UsersConfig
from users.views import UserUpdateAPIView, PaymentListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('profile/update/<int:pk>/', UserUpdateAPIView.as_view(), name='user_update'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),
]

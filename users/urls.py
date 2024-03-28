from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserCreateAPIView, UserRetrieveAPIView, UserUpdateAPIView, UserDestroyAPIView, \
    PaymentListAPIView, UserListAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('list/', UserListAPIView.as_view(), name='user_list'),
    path('user/create/', UserCreateAPIView.as_view(), name='user_create'),
    path('user/<int:pk>/', UserRetrieveAPIView.as_view(), name='user_detail'),
    path('user/<int:pk>/update/', UserUpdateAPIView.as_view(), name='user_update'),
    path('user/<int:pk>/delete/', UserDestroyAPIView.as_view(), name='user_delete'),

    path('payment/', PaymentListAPIView.as_view(), name='payment_list'),

    # tokens
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]


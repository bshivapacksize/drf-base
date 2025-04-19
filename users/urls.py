from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.views import UserRegisterView, UserProfileView

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", UserRegisterView.as_view(), name="user_register"),
    # path('me/<uuid:username>', UserProfileView.as_view(), name="user_profile")
    path("me", UserProfileView.as_view(), name="user_profile"),
]

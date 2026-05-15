from django.urls import path
from .views import (
    ProfileView,
    confirmPasswordReset,
    healthChecker,
    loginUser,
    refreshAccessToken,
    registerUser,
    requestPasswordReset,
    validatePasswordResetToken,
)

urlpatterns = [
    path('health', healthChecker),
    path('register', registerUser),
    path('login', loginUser),
    path('password-reset/request', requestPasswordReset),
    path('password-reset/validate/<str:token>', validatePasswordResetToken),
    path('password-reset/confirm', confirmPasswordReset),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/<int:user_id>/', ProfileView.as_view(), name='profile-by-id'),
    path('refresh/', refreshAccessToken)
]

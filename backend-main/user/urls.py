from django.urls import path
from .views import LoginView, UserRegistrationView, LogoutView  # Import LogoutView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),  # Added logout endpoint
]

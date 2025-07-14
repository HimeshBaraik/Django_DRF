from django.urls import path
from .views import RegisterView, JWTLoginView, LogoutView, DashboardView, ProfileView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', JWTLoginView.as_view(), name='jwt-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', ProfileView.as_view(), name='profile'),
]

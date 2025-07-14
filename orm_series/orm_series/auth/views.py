from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Register
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        email = request.data.get("email")

        # --- ADDED VALIDATION CHECKS ---
        if not username:
            return Response({"error": "Username is required."}, status=status.HTTP_400_BAD_REQUEST)
        if not password:
            return Response({"error": "Password is required."}, status=status.HTTP_400_BAD_REQUEST)
        # --- END ADDED VALIDATION CHECKS ---


        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # The email field on Django's default User model is optional.
            # If you want it to be mandatory, you'd need a custom user model or a serializer.
            # For now, we'll pass it as is.
            user = User.objects.create_user(username=username, password=password, email=email)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            # Catch any other unexpected errors during user creation (e.g., database issues)
            # In a real application, you might log 'e' for debugging.
            return Response(
                {"error": f"An unexpected error occurred during user creation: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# Login
class JWTLoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # --- ADDED VALIDATION CHECKS for login ---
        if not username or not password:
            return Response({"error": "Username and password are required."}, status=status.HTTP_400_BAD_REQUEST)
        # --- END ADDED VALIDATION CHECKS ---

        user = authenticate(username=username, password=password)

        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            # This catch-all is fine for a simple example, but in production,
            # you might want to catch specific exceptions (e.g., TokenError)
            # and return more specific error messages/status codes.
            return Response(status=status.HTTP_400_BAD_REQUEST)

# Dashboard
class DashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": f"Welcome {request.user.username}!"})

# Profile
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "is_staff": user.is_staff
        })


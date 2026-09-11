"""
Account API Views - Authentication endpoints
"""

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from datetime import timedelta
import hashlib
from .serializers import (
    UserSerializer, RegisterSerializer, LoginSerializer,
    ChangePasswordSerializer, ForgotPasswordSerializer, ResetPasswordSerializer,
    ProfileUpdateSerializer
)
from .models import PasswordResetToken


ROLE_DASHBOARD_PATHS = {
    "admin": "/dashboard/admin",
    "doctor": "/dashboard/doctor",
    "nurse": "/dashboard/nurse",
    "care_assistant": "/dashboard/care-assistant",
    "family": "/dashboard",
}

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """POST /api/register/ - Create new user account"""
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'dashboard_path': ROLE_DASHBOARD_PATHS.get(user.role, "/dashboard"),
        }, status=status.HTTP_201_CREATED)

class LoginView(generics.GenericAPIView):
    """POST /api/login/ - Authenticate user and return JWT token"""
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data['password']
        
        user = None
        if email:
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                pass
        if not user and username:
            user = authenticate(username=username, password=password)
        
        if not user:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'dashboard_path': ROLE_DASHBOARD_PATHS.get(user.role, "/dashboard"),
        })

class MeView(generics.RetrieveAPIView):
    """GET /api/me/ - Get current logged-in user data"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    
    def get_object(self):
        return self.request.user

class ChangePasswordView(generics.GenericAPIView):
    """POST /api/change-password/ - Change user password"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response({'old_password': 'Wrong password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password changed successfully'})

class LogoutView(generics.GenericAPIView):
    """POST /api/logout/ - Logout user"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return Response({'message': 'Logged out successfully'})


class ForgotPasswordView(generics.GenericAPIView):
    """POST /api/forgot-password/ - Request password reset token"""
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']

        # Prevent enumeration attacks - always return success
        try:
            user = User.objects.get(email=email)

            # Invalidate previous tokens
            user.password_reset_tokens.filter(is_used=False).update(is_used=True)

            # Generate secure token
            plain_token = PasswordResetToken.generate_token()
            hashed_token = hashlib.sha256(plain_token.encode()).hexdigest()

            # Create reset token with 15 minute expiry
            reset_token = PasswordResetToken.objects.create(
                user=user,
                token=hashed_token,
                token_plain=plain_token,
                expires_at=timezone.now() + timedelta(minutes=15)
            )

            # Construct reset link (frontend handles this)
            reset_link = f"{settings.FRONTEND_URL}/reset-password?token={plain_token}"

            # Send email or log for development
            try:
                send_mail(
                    subject='Password Reset Request',
                    message=f'Click the link to reset your password: {reset_link}\n\nThis link expires in 15 minutes.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False,
                )
            except Exception as e:
                # In development/testing, log the token instead
                print(f'[DEBUG] Password reset token for {email}: {plain_token}')

        except User.DoesNotExist:
            pass

        # Always return success to prevent enumeration
        return Response({
            'message': 'If the email exists, a password reset link has been sent.'
        }, status=status.HTTP_200_OK)


class ResetPasswordView(generics.GenericAPIView):
    """POST /api/reset-password/ - Reset password with token"""
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        plain_token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        # Hash the token and look it up
        hashed_token = hashlib.sha256(plain_token.encode()).hexdigest()

        try:
            reset_token = PasswordResetToken.objects.get(token=hashed_token)
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'error': 'Invalid or expired reset token'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate token
        if not reset_token.is_valid():
            return Response(
                {'error': 'Reset token is expired or already used'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update password
        user = reset_token.user
        user.set_password(new_password)
        user.save()

        # Mark token as used
        reset_token.mark_as_used()

        return Response({
            'message': 'Password reset successfully. You can now login with your new password.'
        }, status=status.HTTP_200_OK)


class ProfileUpdateView(generics.UpdateAPIView):
    """PATCH /api/profile/ - Update user profile (name, email, phone, job title, image)"""
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileUpdateSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)
        self.partial = partial
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(UserSerializer(instance).data, status=status.HTTP_200_OK)

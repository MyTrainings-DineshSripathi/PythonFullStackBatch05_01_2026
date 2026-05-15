from django.conf import settings
from django.contrib.auth import get_user_model
import logging
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.shortcuts import get_object_or_404
from .otp_service import OTPService
from .password_reset_service import PasswordResetService
from .serializers import (
    LoginSerializer,
    PasswordResetConfirmSerializer,
    PasswordResetRequestSerializer,
    RegisterSerializer,
    UserProfileSerializer,
    UserProfileUpdateSerializer,
)
from jobs.email_service import EmailService
from jobs.models import Job, JobApplication
from jobs.utils import send_user_notification

User = get_user_model()
logger = logging.getLogger(__name__)


def build_auth_response(user, request):
    refresh_token = RefreshToken.for_user(user)
    return {
        "accessToken": str(refresh_token.access_token),
        "refreshToken": str(refresh_token),
        "role": user.role,
        "user": UserProfileSerializer(user, context={'request': request}).data,
    }

@api_view(['GET'])
def healthChecker(request):
    return Response({
        "status" : "Working"
    })

@api_view(['POST'])
def registerUser(request):
    serializer = RegisterSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        email_sent = True

        try:
            EmailService.send_welcome_email(user.email, user.fullname, user.role)
        except Exception:
            email_sent = False
            logger.exception("Failed to send welcome email for userId=%s", user.userId)
        
        return Response({
            "message": "User registered successfully" if email_sent else "User registered successfully, but the welcome email could not be sent.",
            "email_sent": email_sent,
            "user": serializer.data
        }, status=201) # 201 Created is better than 200
    
    return Response(serializer.errors, status=400)


# login

@api_view(['POST'])
def loginUser(request):
    serializer = LoginSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    user = serializer.validated_data
    otp_code = (request.data.get('otp') or '').strip()

    if otp_code:
        is_valid, message = OTPService.verify_otp(user, otp_code)
        if not is_valid:
            return Response({"message": message}, status=400)

        OTPService.delete_otp(user)
        return Response(build_auth_response(user, request))

    otp = OTPService.create_otp(user)
    try:
        EmailService.send_otp_email(user.email, otp.otp_code, user.fullname)
    except Exception:
        OTPService.delete_otp(user)
        return Response(
            {"message": "We could not send the OTP email right now. Please try again."},
            status=500,
        )

    return Response(
        {
            "message": "OTP sent to your email address.",
            "otp_required": True,
            "email": user.email,
        },
        status=202,
    )


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def _get_user(self, request, user_id=None):
        target_user = request.user if user_id is None else get_object_or_404(type(request.user), userId=user_id)
        if target_user.userId != request.user.userId:
            return None
        return target_user

    def _build_stats(self, user):
        if user.role == 'HR':
            jobs = Job.objects.filter(posted_by=user)
            applications = JobApplication.objects.filter(job__posted_by=user)
            return {
                "total_jobs_posted": jobs.count(),
                "total_applications_received": applications.count(),
                "accepted_applications": applications.filter(status='accepted').count(),
                "rejected_applications": applications.filter(status='rejected').count(),
            }

        applications = JobApplication.objects.filter(applicant=user)
        return {
            "total_jobs_applied": applications.count(),
            "accepted_applications": applications.filter(status='accepted').count(),
            "rejected_applications": applications.filter(status='rejected').count(),
            "pending_applications": applications.exclude(status__in=['accepted', 'rejected']).count(),
        }

    def _split_name(self, fullname):
        name_parts = (fullname or '').split(' ', 1)
        return {
            "first_name": name_parts[0] if name_parts else '',
            "last_name": name_parts[1] if len(name_parts) > 1 else '',
        }

    def get(self, request, user_id=None):
        user = self._get_user(request, user_id)
        if not user:
            return Response({"message": "Unauthorized"}, status=403)

        profile_data = UserProfileSerializer(user, context={'request': request}).data
        return Response({
            **profile_data,
            **self._split_name(user.fullname),
            "stats": self._build_stats(user),
        })

    def patch(self, request, user_id=None):
        user = self._get_user(request, user_id)
        if not user:
            return Response({"message": "Unauthorized"}, status=403)

        serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            profile_data = UserProfileSerializer(user, context={'request': request}).data
            send_user_notification(
                user.userId,
                'profile_updated',
                {
                    'message': 'Your profile was updated successfully.',
                    'user': profile_data,
                }
            )
            return Response({
                "message": "Profile updated successfully",
                "user": profile_data,
                "stats": self._build_stats(user),
            })

    def delete(self, request, user_id=None):
        user = self._get_user(request, user_id)
        if not user:
            return Response({"message": "Unauthorized"}, status=403)

        send_user_notification(
            user.userId,
            'profile_deleted',
            {
                'message': 'Your profile has been deleted.',
                'userId': user.userId,
            }
        )

        user.delete()
        return Response({"message": "Profile deleted successfully"}, status=200)

        return Response(serializer.errors, status=400)


@api_view(['POST'])
def refreshAccessToken(request):
    refresh_token = request.data.get('refresh_token')
    if not refresh_token:
        return Response({"error": "Refresh token is required"}, status=400)
    
    try:
        token = RefreshToken(refresh_token)
        new_access_token = str(token.access_token)
        return Response({
            "accessToken": new_access_token
        })
    except TokenError:
        return Response({"error": "Invalid refresh token"}, status=400)


@api_view(['POST'])
def requestPasswordReset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    email = serializer.validated_data['email'].strip().lower()
    generic_message = "If an account exists for this email, a password reset link has been sent."
    user = User.objects.filter(email__iexact=email).first()

    if not user:
        return Response({"message": generic_message})

    reset_token = PasswordResetService.create_reset_token(user)
    frontend_url = request.headers.get('Origin') or getattr(settings, 'FRONTEND_URL', 'http://localhost:5173')
    frontend_url = frontend_url.rstrip('/')
    reset_url = f"{frontend_url}/reset-password/{reset_token.token}"

    try:
        EmailService.send_password_reset_email(
            user.email,
            reset_token.token,
            user.fullname,
            reset_url,
        )
    except Exception:
        PasswordResetService.delete_reset_token(user)
        return Response(
            {"message": "We could not send the password reset email right now. Please try again."},
            status=500,
        )

    return Response({"message": generic_message})


@api_view(['GET'])
def validatePasswordResetToken(request, token):
    reset_token = PasswordResetService.get_reset_token(token)
    if not reset_token:
        return Response({"message": "Invalid or expired reset link."}, status=400)

    return Response({"message": "Reset token is valid."})


@api_view(['POST'])
def confirmPasswordReset(request):
    serializer = PasswordResetConfirmSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    reset_token = serializer.validated_data['reset_token']
    success, message = PasswordResetService.validate_and_reset_password(
        reset_token.token,
        serializer.validated_data['password'],
    )

    status_code = 200 if success else 400
    return Response({"message": message}, status=status_code)

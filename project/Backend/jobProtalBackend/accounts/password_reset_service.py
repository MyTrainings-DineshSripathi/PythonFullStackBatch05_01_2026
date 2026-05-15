"""Password Reset Service for secure password reset flow"""
from datetime import timedelta
from django.utils import timezone
from .models import PasswordResetToken, User


class PasswordResetService:
    """Service to handle password reset token generation and validation"""
    
    PASSWORD_RESET_VALIDITY_HOURS = 24  # Token valid for 24 hours
    
    @classmethod
    def create_reset_token(cls, user):
        """Create a password reset token for user"""
        # Delete existing reset tokens for this user
        PasswordResetToken.objects.filter(user=user).delete()
        
        token = PasswordResetToken.generate_token()
        expires_at = timezone.now() + timedelta(hours=cls.PASSWORD_RESET_VALIDITY_HOURS)
        
        reset_token = PasswordResetToken.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )
        
        return reset_token
    
    @staticmethod
    def get_reset_token(token):
        """Get a reset token object if it exists and is valid"""
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
            if not reset_token.is_valid():
                return None
            return reset_token
        except PasswordResetToken.DoesNotExist:
            return None
    
    @staticmethod
    def validate_and_reset_password(token_string, new_password):
        """Validate token and reset user password"""
        reset_token = PasswordResetService.get_reset_token(token_string)
        
        if not reset_token:
            return False, "Invalid or expired reset token"
        
        try:
            user = reset_token.user
            user.set_password(new_password)
            user.save()
            
            # Mark token as used
            reset_token.is_used = True
            reset_token.save()
            
            return True, "Password reset successfully"
        
        except Exception as e:
            return False, f"Error resetting password: {str(e)}"
    
    @staticmethod
    def delete_reset_token(user):
        """Delete reset token for user"""
        PasswordResetToken.objects.filter(user=user).delete()

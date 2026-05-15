"""OTP Service for email verification and authentication"""
import random
from datetime import timedelta
from django.utils import timezone
from .models import OTP, User


class OTPService:
    """Service to handle OTP generation, validation, and verification"""
    
    OTP_VALIDITY_MINUTES = 10  # OTP valid for 10 minutes
    OTP_LENGTH = 6
    
    @staticmethod
    def generate_otp_code():
        """Generate a 6-digit OTP code"""
        return ''.join([str(random.randint(0, 9)) for _ in range(OTPService.OTP_LENGTH)])
    
    @classmethod
    def create_otp(cls, user):
        """Create or update OTP for user"""
        otp_code = cls.generate_otp_code()
        expires_at = timezone.now() + timedelta(minutes=cls.OTP_VALIDITY_MINUTES)
        
        # Delete existing OTP if it exists
        OTP.objects.filter(user=user).delete()
        
        # Create new OTP
        otp = OTP.objects.create(
            user=user,
            otp_code=otp_code,
            expires_at=expires_at
        )
        
        return otp
    
    @staticmethod
    def get_user_otp(user):
        """Get current valid OTP for user"""
        try:
            otp = OTP.objects.get(user=user)
            if not otp.is_valid():
                return None
            return otp
        except OTP.DoesNotExist:
            return None
    
    @staticmethod
    def verify_otp(user, otp_code):
        """Verify OTP code for user"""
        try:
            otp = OTP.objects.get(user=user)
            
            if not otp.is_valid():
                return False, "OTP has expired or already verified"
            
            if otp.otp_code != otp_code:
                otp.increment_attempts()
                remaining_attempts = otp.max_attempts - otp.attempts
                if remaining_attempts <= 0:
                    return False, "Maximum OTP attempts exceeded"
                return False, f"Invalid OTP. Remaining attempts: {remaining_attempts}"
            
            # Mark OTP as verified
            otp.is_verified = True
            otp.save()
            
            return True, "OTP verified successfully"
        
        except OTP.DoesNotExist:
            return False, "OTP not found"
    
    @staticmethod
    def delete_otp(user):
        """Delete OTP for user"""
        OTP.objects.filter(user=user).delete()

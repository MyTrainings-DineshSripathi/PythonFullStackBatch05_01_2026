from django.core import mail
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase
from unittest.mock import patch

from .models import OTP, PasswordResetToken, User


@override_settings(
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    FRONTEND_URL='http://localhost:5173',
)
class AuthSecurityFlowsTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email='seeker@example.com',
            password='StrongPass123!',
            fullname='Seeker User',
            role='SEEKER',
        )

    def test_registration_sends_welcome_email(self):
        response = self.client.post(
            '/user/register',
            {
                'email': 'newuser@example.com',
                'password': 'StrongPass123!',
                'fullname': 'New User',
                'role': 'SEEKER',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['email_sent'])
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, ['newuser@example.com'])
        self.assertIn('Welcome to Job Portal', mail.outbox[0].subject)

    @patch('accounts.views.EmailService.send_welcome_email', side_effect=Exception('SMTP error'))
    def test_registration_still_succeeds_when_welcome_email_fails(self, _mock_send):
        response = self.client.post(
            '/user/register',
            {
                'email': 'mailfail@example.com',
                'password': 'StrongPass123!',
                'fullname': 'Mail Fail',
                'role': 'SEEKER',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertFalse(response.data['email_sent'])
        self.assertTrue(User.objects.filter(email='mailfail@example.com').exists())

    def test_login_requires_otp_before_tokens_are_issued(self):
        response = self.client.post(
            '/user/login',
            {
                'email': self.user.email,
                'password': 'StrongPass123!',
            },
            format='json',
        )

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        self.assertTrue(response.data['otp_required'])
        self.assertNotIn('accessToken', response.data)
        self.assertEqual(len(mail.outbox), 1)

        otp = OTP.objects.get(user=self.user)
        verify_response = self.client.post(
            '/user/login',
            {
                'email': self.user.email,
                'password': 'StrongPass123!',
                'otp': otp.otp_code,
            },
            format='json',
        )

        self.assertEqual(verify_response.status_code, status.HTTP_200_OK)
        self.assertIn('accessToken', verify_response.data)
        self.assertIn('refreshToken', verify_response.data)
        self.assertFalse(OTP.objects.filter(user=self.user).exists())

    def test_password_reset_request_sends_email_and_updates_password(self):
        request_response = self.client.post(
            '/user/password-reset/request',
            {'email': self.user.email},
            format='json',
        )

        self.assertEqual(request_response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mail.outbox), 1)

        reset_token = PasswordResetToken.objects.get(user=self.user)
        self.assertIn(reset_token.token, mail.outbox[0].alternatives[0][0])

        validate_response = self.client.get(
            f'/user/password-reset/validate/{reset_token.token}'
        )
        self.assertEqual(validate_response.status_code, status.HTTP_200_OK)

        confirm_response = self.client.post(
            '/user/password-reset/confirm',
            {
                'token': reset_token.token,
                'password': 'NewStrongPass123!',
                'confirm_password': 'NewStrongPass123!',
            },
            format='json',
        )

        self.assertEqual(confirm_response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        reset_token.refresh_from_db()
        self.assertTrue(self.user.check_password('NewStrongPass123!'))
        self.assertTrue(reset_token.is_used)

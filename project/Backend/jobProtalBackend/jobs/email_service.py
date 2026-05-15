from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags


class EmailService:
    @staticmethod
    def send_welcome_email(email, fullname, role):
        """Send welcome email after successful registration"""
        subject = 'Welcome to Job Portal'

        context = {
            'fullname': fullname,
            'email': email,
            'role': role,
        }

        html_message = render_to_string('emails/welcome_email.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_job_application_notification(seeker_email, job_title, company_name):
        """Send email to seeker when they apply for a job"""
        subject = f'Application Submitted - {job_title}'

        context = {
            'job_title': job_title,
            'company_name': company_name,
            'seeker_email': seeker_email,
        }

        html_message = render_to_string('emails/job_application.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seeker_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_application_status_update(seeker_email, job_title, company_name, status):
        """Send email to seeker when application status changes"""
        subject = f'Application Status Update - {job_title}'

        context = {
            'job_title': job_title,
            'company_name': company_name,
            'status': status,
            'seeker_email': seeker_email,
        }

        html_message = render_to_string('emails/application_status_update.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seeker_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_new_job_notification(seeker_email, job_title, company_name):
        """Send email to seekers when a new job is posted"""
        subject = f'New Job Opportunity - {job_title}'

        context = {
            'job_title': job_title,
            'company_name': company_name,
            'seeker_email': seeker_email,
        }

        html_message = render_to_string('emails/new_job_posted.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[seeker_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_hr_application_notification(hr_email, job_title, applicant_name):
        """Send email to HR when someone applies for their job"""
        subject = f'New Application Received - {job_title}'

        context = {
            'job_title': job_title,
            'applicant_name': applicant_name,
            'hr_email': hr_email,
        }

        html_message = render_to_string('emails/hr_new_application.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[hr_email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_otp_email(email, otp_code, fullname):
        """Send OTP email for email verification"""
        subject = 'Your OTP Code - Job Portal'

        context = {
            'otp_code': otp_code,
            'fullname': fullname,
            'email': email,
            'validity_minutes': 10,
        }

        html_message = render_to_string('emails/otp_verification.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

    @staticmethod
    def send_password_reset_email(email, reset_token, fullname, reset_url):
        """Send password reset email"""
        subject = 'Password Reset Request - Job Portal'

        context = {
            'fullname': fullname,
            'email': email,
            'reset_token': reset_token,
            'reset_url': reset_url,
            'validity_hours': 24,
        }

        html_message = render_to_string('emails/password_reset.html', context)
        plain_message = strip_tags(html_message)

        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            html_message=html_message,
            fail_silently=False,
        )

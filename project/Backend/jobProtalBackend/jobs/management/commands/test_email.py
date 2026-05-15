from django.core.management.base import BaseCommand
from jobs.email_service import EmailService


class Command(BaseCommand):
    help = 'Test email sending functionality'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Email address to send test to')

    def handle(self, *args, **options):
        email = options['email']

        try:
            # Test job application notification
            EmailService.send_job_application_notification(
                email,
                'Software Engineer',
                'Tech Company Inc.'
            )
            self.stdout.write(self.style.SUCCESS(f'Test email sent successfully to {email}'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Failed to send email: {e}'))
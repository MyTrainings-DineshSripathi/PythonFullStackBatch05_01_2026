# from django.shortcuts import render
# Create your views here.

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db import models
from .serializers import JobSerializer, JobListSerializer, JobApplicationSerializer, ReportSerializer, PermissionSerializer
from .permissions import IsHR, IsSeeker, IsAdmin, IsModeratorOrAdmin, CanReportJob, CanManageReports
from .models import (
    Job,
    JobSkill,
    JobDescription,
    JobResponsibility,
    JobApplication,
    Report,
    ModerationLog,
    UserStrike,
    Notification,
    Permission,
)
from .utils import send_user_notification
from accounts.models import User
from .email_service import EmailService
from django.utils import timezone
from datetime import timedelta

one_year_ago = timezone.now() - timedelta(days=365)

class PostJobView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsAuthenticated]

    def post(self, request):
        return create_job_post(request, posting_source='post')


class ShareJobView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        return create_job_post(request, posting_source='share')


def create_job_post(request, posting_source):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            job = serializer.save(posted_by=request.user, posting_source=posting_source)  # 👈 track who posted
            
            # Send notification to all seekers about the new job
            seekers = User.objects.filter(role='SEEKER')
            for seeker in seekers:
                send_user_notification(
                    seeker.userId,
                    'new_job',
                    {
                        'message': f'New job posted: {job.title}',
                        'job_id': job.id,
                        'job': JobListSerializer(job).data,
                    }
                )

                # Send email notification to seeker
                try:
                    EmailService.send_new_job_notification(
                        seeker.email,
                        job.title,
                        job.company
                    )
                except Exception as e:
                    print(f"Email sending failed for {seeker.email}: {e}")
            
            return Response(
                {
                    "message": "Job posted successfully",
                    "job_id": job.id,
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            {
                "message": "Invalid data",
                "errors": serializer.errors,
            },
            status=status.HTTP_400_BAD_REQUEST
        )

class getAllJobsView(APIView):

    def get(self, request):
        jobs = Job.objects.prefetch_related(
            'skills',
            'job_descriptions',
            'roles_and_responsibilities',
        ).select_related('posted_by').filter(
            posted_at__gte=one_year_ago,    # 👈 gte = greater than or equal to
            is_active=True,
        ).order_by('-posted_at')   # latest first

        serializer = JobListSerializer(jobs, many=True)

        return Response(
            {
                "message": "Jobs fetched successfully",
                "count"  : jobs.count(),
                "jobs"   : serializer.data,
            },
            status=status.HTTP_200_OK
        )


class GetJobByIdView(APIView):
    """Fetch a single job by ID with all its details"""

    def get(self, request, job_id):
        try:
            job = Job.objects.prefetch_related(
                'skills',
                'job_descriptions',
                'roles_and_responsibilities',
            ).select_related('posted_by').get(id=job_id)
        except Job.DoesNotExist:
            return Response(
                {"message": "Job not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobListSerializer(job)

        return Response(
            {
                "message": "Job fetched successfully",
                "job": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class ApplyJobView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"message": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        # Check if user already applied
        if JobApplication.objects.filter(job=job, applicant=request.user).exists():
            return Response({"message": "You have already applied for this job"}, status=status.HTTP_400_BAD_REQUEST)
        print(request.data)
        serializer = JobApplicationSerializer(data=request.data)
        if serializer.is_valid():
            application = serializer.save(job=job, applicant=request.user)

            send_user_notification(
                job.posted_by.userId,
                'new_application',
                {
                    'message': 'New job application received',
                    'job_id': job.id,
                    'application': JobApplicationSerializer(application).data,
                }
            )

            # Send email notifications
            try:
                # Email to seeker confirming application submission
                EmailService.send_job_application_notification(
                    request.user.email,
                    job.title,
                    job.company
                )

                # Email to HR about new application
                EmailService.send_hr_application_notification(
                    job.posted_by.email,
                    job.title,
                    request.user.fullname
                )
            except Exception as e:
                # Log email error but don't fail the application
                print(f"Email sending failed: {e}")

            return Response({
                "message": "Application submitted successfully",
                "application_id": application.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HRJobsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHR]

    def get(self, request):
        jobs = Job.objects.filter(posted_by=request.user).prefetch_related('applications', 'applications__applicant').order_by('-posted_at')
        print(jobs)
        data = []
        for job in jobs:
            applications = job.applications.all()
            data.append({
                'id': job.id,
                'job_code': job.job_code,
                'title': job.title,
                'company': job.company,
                'posting_source': job.posting_source,
                'posted_at': job.posted_at,
                'applications_count': applications.count(),
                'applications': JobApplicationSerializer(applications, many=True).data
            })
        return Response({
            "jobs": data
        }, status=status.HTTP_200_OK)


class HRStatsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHR]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        month_start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        jobs = Job.objects.filter(posted_by=request.user)
        total_jobs = jobs.count()
        jobs_this_month = jobs.filter(posted_at__gte=month_start).count()
        applications = JobApplication.objects.filter(job__posted_by=request.user)
        total_applications = applications.count()
        new_applications_today = applications.filter(applied_at__gte=today_start).count()
        return Response({
            "total_jobs": total_jobs,
            "total_applications": total_applications,
            "new_applications_today": new_applications_today,
            "jobs_this_month": jobs_this_month
        }, status=status.HTTP_200_OK)


class SeekerDashboardView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        now = timezone.now()
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)

        applications = JobApplication.objects.filter(applicant=request.user).select_related('job').order_by('-applied_at')

        total_jobs_applied = applications.count()
        total_jobs_applied_today = applications.filter(applied_at__gte=today_start).count()
        new_jobs_today = Job.objects.filter(posted_at__gte=today_start).count()
        accepted_count = applications.filter(status='accepted').count()
        rejected_count = applications.filter(status='rejected').count()
        no_action_count = applications.exclude(status__in=['accepted', 'rejected']).count()

        application_rows = []
        for application in applications:
            application_rows.append({
                'id': application.id,
                'job_title': application.job.title,
                'company': application.job.company,
                'location': application.job.location,
                'applied_at': application.applied_at,
                'status': application.status,
            })

        shared_jobs = Job.objects.filter(
            posted_by=request.user,
            posting_source='share',
        ).prefetch_related('applications', 'applications__applicant').order_by('-posted_at')

        shared_job_rows = []
        for job in shared_jobs:
            job_applications = job.applications.all()
            shared_job_rows.append({
                'id': job.id,
                'job_code': job.job_code,
                'title': job.title,
                'company': job.company,
                'posted_at': job.posted_at,
                'applications_count': job_applications.count(),
                'applications': JobApplicationSerializer(job_applications, many=True).data,
            })

        return Response({
            "stats": {
                "total_jobs_applied": total_jobs_applied,
                "total_jobs_applied_today": total_jobs_applied_today,
                "new_jobs_today": new_jobs_today,
                "accepted_count": accepted_count,
                "rejected_count": rejected_count,
                "no_action_count": no_action_count,
                "shared_jobs_count": shared_jobs.count(),
                "shared_job_applications_count": sum(job['applications_count'] for job in shared_job_rows),
            },
            "applications": application_rows,
            "shared_jobs": shared_job_rows,
        }, status=status.HTTP_200_OK)


class UpdateApplicationStatusView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHR]

    def patch(self, request, application_id):
        try:
            application = JobApplication.objects.get(id=application_id)
            # Verify HR owns the job
            if application.job.posted_by != request.user:
                return Response({"message": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
            
            new_status = request.data.get('status')
            if new_status not in ['pending', 'reviewed', 'accepted', 'rejected']:
                return Response({"message": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
            
            application.status = new_status
            application.save()

            payload = {
                'message': f"Application status updated to {new_status}",
                'application': JobApplicationSerializer(application).data,
            }
            send_user_notification(application.applicant.userId, 'application_status_updated', payload)
            send_user_notification(application.job.posted_by.userId, 'application_status_updated', payload)

            # Send email notification to applicant
            try:
                EmailService.send_application_status_update(
                    application.applicant.email,
                    application.job.title,
                    application.job.company,
                    new_status
                )
            except Exception as e:
                print(f"Email sending failed: {e}")
            
            return Response({
                "message": "Status updated successfully",
                "application": JobApplicationSerializer(application).data
            }, status=status.HTTP_200_OK)
        except JobApplication.DoesNotExist:
            return Response({"message": "Application not found"}, status=status.HTTP_404_NOT_FOUND)


# Moderation Views
class ReportJobView(APIView):
    """
    Report a job for abuse, incorrect details, or scam.
    Only seekers can report jobs.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanReportJob]

    def post(self, request, job_id):
        try:
            job = Job.objects.get(id=job_id)
        except Job.DoesNotExist:
            return Response({"message": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ReportSerializer(data=request.data)
        if serializer.is_valid():
            report = serializer.save(job=job, reporter=request.user)
            
            # Send notification to admins/moderators
            admins_and_moderators = User.objects.filter(
                models.Q(role='ADMIN') | models.Q(is_moderator=True)
            )
            for admin in admins_and_moderators:
                send_user_notification(
                    admin.userId,
                    'new_report',
                    {
                        'message': f'New report: {report.reason}',
                        'report_id': report.id,
                        'job_id': job.id,
                    }
                )
            
            return Response({
                "message": "Report submitted successfully",
                "report_id": report.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListReportsView(APIView):
    """
    List all reports. Only admin/moderator can access this.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanManageReports]

    def get(self, request):
        # Optional: filter by status
        status_filter = request.query_params.get('status', None)
        reports = Report.objects.select_related('job', 'reporter').order_by('-created_at')
        
        if status_filter:
            reports = reports.filter(status=status_filter)
        
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "count": reports.count(),
            "reports": serializer.data
        })


class ReviewReportView(APIView):
    """
    Review a report and take action. Only admin/moderator can access this.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [CanManageReports]

    def patch(self, request, report_id):
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return Response({"message": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

        action = request.data.get('action')  # 'reviewed', 'resolved', 'dismissed'
        action_taken = request.data.get('action_taken', '')
        
        if action not in ['reviewed', 'resolved', 'dismissed']:
            return Response({"message": "Invalid action"}, status=status.HTTP_400_BAD_REQUEST)

        report.status = action
        report.reviewed_by = request.user
        report.reviewed_at = timezone.now()
        report.action_taken = action_taken
        
        if action == 'resolved':
            # Hide the job if action is resolved
            report.job.is_active = False
            report.job.save()
            
            # Add strike to user who posted the job
            UserStrike.objects.create(
                user=report.job.posted_by,
                reason=f"Job reported and resolved: {report.reason}",
                strike_level=1
            )
            
            # Log moderation action
            ModerationLog.objects.create(
                job=report.job,
                moderator=request.user,
                action='hide_job',
                details={
                    'reason': report.reason,
                    'report_id': report.id,
                    'action_taken': action_taken
                }
            )

        report.save()

        return Response({
            "message": f"Report marked as {action}",
            "report": ReportSerializer(report).data
        })


class UserReportsView(APIView):
    """
    Get reports submitted by the current user (only for seekers).
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeeker]

    def get(self, request):
        reports = Report.objects.filter(reporter=request.user).select_related('job').order_by('-created_at')
        serializer = ReportSerializer(reports, many=True)
        return Response({
            "count": reports.count(),
            "reports": serializer.data
        })


# Dashboard Tab Views
class SeekerApplicationsTabView(APIView):
    """
    Get jobs that the seeker has applied to (for 'Job Applications' tab).
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeeker]

    def get(self, request):
        applications = JobApplication.objects.filter(
            applicant=request.user
        ).select_related('job').order_by('-applied_at')

        application_data = []
        for app in applications:
            application_data.append({
                'id': app.id,
                'job_id': app.job.id,
                'job_title': app.job.title,
                'company': app.job.company,
                'location': app.job.location,
                'job_type': app.job.type,
                'salary': app.job.salary,
                'applied_at': app.applied_at,
                'status': app.status,
                'job_code': app.job.job_code,
            })

        return Response({
            "count": applications.count(),
            "applications": application_data
        })


class SeekerAllJobsTabView(APIView):
    """
    Get all available jobs in the system (for 'Shared Jobs' tab).
    This shows jobs posted by all HR users that are visible to all seekers.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsSeeker]

    def get(self, request):
        # Get all active jobs from the last year
        jobs = Job.objects.filter(
            posted_at__gte=one_year_ago,
            is_active=True,
        ).prefetch_related(
            'skills',
            'job_descriptions',
            'roles_and_responsibilities',
        ).select_related('posted_by').order_by('-posted_at')

        # Filter out jobs where user has already applied
        applied_job_ids = JobApplication.objects.filter(
            applicant=request.user
        ).values_list('job_id', flat=True)
        
        available_jobs = jobs.exclude(id__in=applied_job_ids)

        serializer = JobListSerializer(available_jobs, many=True)

        return Response({
            "count": available_jobs.count(),
            "jobs": serializer.data
        })


class HRApplicationsTabView(APIView):
    """
    Get applications received on jobs posted by current HR (for 'My Applications' tab).
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHR]

    def get(self, request):
        # Get all applications on jobs posted by current HR
        applications = JobApplication.objects.filter(
            job__posted_by=request.user
        ).select_related('job', 'applicant').order_by('-applied_at')

        application_data = []
        for app in applications:
            application_data.append({
                'id': app.id,
                'job_id': app.job.id,
                'job_title': app.job.title,
                'job_code': app.job.job_code,
                'applicant_name': app.applicant.fullname,
                'applicant_email': app.applicant.email,
                'applicant_id': app.applicant.userId,
                'applied_at': app.applied_at,
                'status': app.status,
            })

        return Response({
            "count": applications.count(),
            "applications": application_data
        })


class HRSharedApplicationsTabView(APIView):
    """
    Get applications on jobs shared by the current HR (for 'Shared Applications' tab).
    Only the HR user who shared the job can see the applications for that shared job.
    """
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsHR]

    def get(self, request):
        shared_jobs = Job.objects.filter(
            posted_by=request.user,
            posting_source='share',
        ).prefetch_related('applications', 'applications__applicant').order_by('-posted_at')

        application_data = []
        for job in shared_jobs:
            for app in job.applications.all():
                application_data.append({
                    'id': app.id,
                    'job_id': job.id,
                    'job_title': job.title,
                    'job_code': job.job_code,
                    'job_company': job.company,
                    'applicant_name': app.applicant.fullname,
                    'applicant_email': app.applicant.email,
                    'applicant_id': app.applicant.userId,
                    'applied_at': app.applied_at,
                    'status': app.status,
                })

        return Response({
            "count": len(application_data),
            "applications": application_data
        }, status=status.HTTP_200_OK)


# Notification Views
class NotificationListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user=request.user).order_by('-created_at')
        serializer = NotificationSerializer(notifications, many=True)
        return Response(serializer.data)


class MarkNotificationReadView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        try:
            notification = Notification.objects.get(id=notification_id, user=request.user)
            notification.is_read = True
            notification.save()
            return Response({"message": "Notification marked as read"})
        except Notification.DoesNotExist:
            return Response({"message": "Notification not found"}, status=status.HTTP_404_NOT_FOUND)

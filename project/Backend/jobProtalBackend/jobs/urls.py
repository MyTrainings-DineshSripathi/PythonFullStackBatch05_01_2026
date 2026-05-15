from django.urls import path, include
from .views import (
    PostJobView,
    ShareJobView,
    getAllJobsView,
    GetJobByIdView,
    ApplyJobView,
    HRJobsView,
    HRStatsView,
    SeekerDashboardView,
    UpdateApplicationStatusView,
    ReportJobView,
    ListReportsView,
    ReviewReportView,
    UserReportsView,
    SeekerApplicationsTabView,
    SeekerAllJobsTabView,
    HRApplicationsTabView,
    HRSharedApplicationsTabView,
    NotificationListView,
    MarkNotificationReadView,
)

urlpatterns = [
    path('post/', PostJobView.as_view(), name='post-job'),
    path('share/', ShareJobView.as_view(), name='share-job'),
    path('all/', getAllJobsView.as_view(), name='get-all-jobs'),
    path('<int:job_id>/', GetJobByIdView.as_view(), name='get-job-by-id'),
    path('<int:job_id>/apply/', ApplyJobView.as_view(), name='apply-job'),
    
    # HR endpoints
    path('hr/jobs/', HRJobsView.as_view(), name='hr-jobs'),
    path('hr/stats/', HRStatsView.as_view(), name='hr-stats'),
    path('hr/applications/', HRApplicationsTabView.as_view(), name='hr-applications'),
    path('hr/shared-applications/', HRSharedApplicationsTabView.as_view(), name='hr-shared-applications'),
    
    # Seeker endpoints
    path('seeker/dashboard/', SeekerDashboardView.as_view(), name='seeker-dashboard'),
    path('seeker/applications/', SeekerApplicationsTabView.as_view(), name='seeker-applications'),
    path('seeker/all-jobs/', SeekerAllJobsTabView.as_view(), name='seeker-all-jobs'),
    
    # Application & Status endpoints
    path('application/<int:application_id>/status/', UpdateApplicationStatusView.as_view(), name='update-application-status'),
    
    # Report endpoints
    path('<int:job_id>/report/', ReportJobView.as_view(), name='report-job'),
    path('reports/', ListReportsView.as_view(), name='list-reports'),
    path('reports/<int:report_id>/review/', ReviewReportView.as_view(), name='review-report'),
    path('user/reports/', UserReportsView.as_view(), name='user-reports'),
    
    # Notification endpoints
    path('notifications/', NotificationListView.as_view(), name='notifications'),
    path('notifications/<int:notification_id>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
]

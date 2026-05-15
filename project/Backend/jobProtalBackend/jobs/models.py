# models.py

from django.db import models
import random

class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Remote', 'Remote'),
        ('Contract', 'Contract'),
    ]

    APPLY_SOURCE_CHOICES = [
        ('hire_flow', 'Krowdly'),
        ('company_site', 'Company Site'),
    ]

    POSTING_SOURCE_CHOICES = [
        ('post', 'Post'),
        ('share', 'Share'),
    ]

    title          = models.CharField(max_length=255)
    job_code       = models.CharField(max_length=20, unique=True, null=True, blank=True)
    company        = models.CharField(max_length=255)
    location       = models.CharField(max_length=255)
    experience     = models.CharField(max_length=50)           # "1", "0-2 Years" etc.
    type           = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full Time')
    salary         = models.CharField(max_length=100)          # keep flexible — "10000" or "6L-10L/yr"
    about_company  = models.TextField()
    apply_source   = models.CharField(max_length=20, choices=APPLY_SOURCE_CHOICES, default='hire_flow')
    posting_source = models.CharField(max_length=20, choices=POSTING_SOURCE_CHOICES, default='post')
    url            = models.URLField(max_length=500, null=True, blank=True)  # null when hire_flow
    posted_at      = models.DateTimeField()
    created_at     = models.DateTimeField(auto_now_add=True)   # when record was inserted
    posted_by      = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='jobs_posted')
    is_active      = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} @ {self.company}"

    def save(self, *args, **kwargs):
        if not self.job_code:
            while True:
                candidate = f"job{random.randint(1000, 999999)}"
                if not type(self).objects.filter(job_code=candidate).exists():
                    self.job_code = candidate
                    break
        super().save(*args, **kwargs)


class JobSkill(models.Model):
    job   = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='skills')
    skill = models.CharField(max_length=100)

    def __str__(self):
        return self.skill


class JobDescription(models.Model):
    job   = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='job_descriptions')
    point = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"JD point {self.order} — {self.job.title}"


class JobResponsibility(models.Model):
    job   = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='roles_and_responsibilities')
    point = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Responsibility {self.order} — {self.job.title}"


class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.applicant.fullname} applied for {self.job.title}"


class Report(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    ]
    
    REPORT_TYPE_CHOICES = [
        ('abuse', 'Abuse/Inappropriate Content'),
        ('job_details_error', 'Job Details Error'),
        ('scam_post', 'Scam Post'),
    ]

    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='reports')
    reporter = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reports')
    report_type = models.CharField(max_length=20, choices=REPORT_TYPE_CHOICES, default='abuse')
    reason = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    reviewed_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='reports_reviewed')
    reviewed_at = models.DateTimeField(null=True, blank=True)
    action_taken = models.CharField(max_length=255, blank=True, help_text="Description of action taken by moderator")

    def __str__(self):
        return f"Report on {self.job.title} by {self.reporter.email}"


class ModerationLog(models.Model):
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='moderation_logs')
    moderator = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='moderation_actions')
    action = models.CharField(max_length=100)
    details = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} on {self.job.title} by {self.moderator.email}"


class UserStrike(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='strikes')
    reason = models.CharField(max_length=255)
    strike_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Strike {self.strike_level} for {self.user.email}: {self.reason}"


class Notification(models.Model):
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class Permission(models.Model):
    """
    Granular permission model for tracking user permissions
    beyond basic role-based access.
    """
    PERMISSION_CHOICES = [
        ('view_reports', 'View Reports'),
        ('manage_reports', 'Manage Reports'),
        ('moderate_jobs', 'Moderate Jobs'),
        ('suspend_users', 'Suspend Users'),
        ('view_analytics', 'View Analytics'),
        ('manage_permissions', 'Manage Permissions'),
    ]
    
    user = models.OneToOneField('accounts.User', on_delete=models.CASCADE, related_name='permissions')
    permissions = models.JSONField(
        default=list,
        help_text="List of permission codes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def has_permission(self, permission_code):
        """Check if user has a specific permission"""
        return permission_code in self.permissions
    
    def add_permission(self, permission_code):
        """Add a permission to the user"""
        if permission_code not in self.permissions:
            self.permissions.append(permission_code)
            self.save()
    
    def remove_permission(self, permission_code):
        """Remove a permission from the user"""
        if permission_code in self.permissions:
            self.permissions.remove(permission_code)
            self.save()
    
    def __str__(self):
        return f"Permissions for {self.user.email}"


    def __str__(self):
        return f"{self.type} notification for {self.user.email}: {self.title}"


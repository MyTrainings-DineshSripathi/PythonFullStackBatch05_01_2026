# models.py

from django.db import models

class Job(models.Model):

    JOB_TYPE_CHOICES = [
        ('Full Time', 'Full Time'),
        ('Part Time', 'Part Time'),
        ('Remote', 'Remote'),
        ('Contract', 'Contract'),
    ]

    APPLY_SOURCE_CHOICES = [
        ('hire_flow', 'HireFlow'),
        ('company_site', 'Company Site'),
    ]

    title          = models.CharField(max_length=255)
    company        = models.CharField(max_length=255)
    location       = models.CharField(max_length=255)
    experience     = models.CharField(max_length=50)           # "1", "0-2 Years" etc.
    type           = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Full Time')
    salary         = models.CharField(max_length=100)          # keep flexible — "10000" or "6L-10L/yr"
    about_company  = models.TextField()
    apply_source   = models.CharField(max_length=20, choices=APPLY_SOURCE_CHOICES, default='hire_flow')
    url            = models.URLField(max_length=500, null=True, blank=True)  # null when hire_flow
    posted_at      = models.DateTimeField()
    created_at     = models.DateTimeField(auto_now_add=True)   # when record was inserted
    posted_by      = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, related_name='jobs_posted')

    def __str__(self):
        return f"{self.title} @ {self.company}"


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
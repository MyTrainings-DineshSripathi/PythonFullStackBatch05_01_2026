# serializers.py

from rest_framework import serializers
from .models import Job, JobSkill, JobDescription, JobResponsibility, JobApplication, Report, ModerationLog, UserStrike, Notification, Permission
from accounts.serializers import UserProfileSerializer

class JobSkillSerializer(serializers.ModelSerializer):
    class Meta:
        model  = JobSkill
        fields = ['skill']

class JobDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model  = JobDescription
        fields = ['point', 'order']

class JobResponsibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = JobResponsibility
        fields = ['point', 'order']

class JobSerializer(serializers.ModelSerializer):
    skills                   = serializers.ListField(child=serializers.CharField(), write_only=True)
    job_description          = serializers.ListField(child=serializers.CharField(), write_only=True)
    roles_and_responsibilities = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model  = Job
        fields = [
            'id', 'job_code', 'title', 'company', 'location', 'experience',
            'type', 'salary', 'about_company', 'apply_source', 'posting_source',
            'url', 'posted_at', 'posted_by',
            'skills', 'job_description', 'roles_and_responsibilities',
        ]
        
        read_only_fields = ['id', 'job_code', 'posted_by', 'posting_source']  # these are set automatically, not by user input

    def create(self, validated_data):
        skills  = validated_data.pop('skills', [])
        jd      = validated_data.pop('job_description', [])
        roles   = validated_data.pop('roles_and_responsibilities', [])

        job = Job.objects.create(**validated_data)

        JobSkill.objects.bulk_create([
            JobSkill(job=job, skill=s) for s in skills
        ])
        JobDescription.objects.bulk_create([
            JobDescription(job=job, point=p, order=i) for i, p in enumerate(jd)
        ])
        JobResponsibility.objects.bulk_create([
            JobResponsibility(job=job, point=p, order=i) for i, p in enumerate(roles)
        ])

        return job

# serializers.py

class JobListSerializer(serializers.ModelSerializer):

    skills                     = serializers.SerializerMethodField()
    job_description            = serializers.SerializerMethodField()
    roles_and_responsibilities = serializers.SerializerMethodField()
    posted_by                  = serializers.StringRelatedField()  # returns username

    class Meta:
        model  = Job
        fields = [
            'id',
            'job_code',
            'title',
            'company',
            'location',
            'experience',
            'type',
            'salary',
            'about_company',
            'apply_source',
            'posting_source',
            'url',
            'posted_at',
            'posted_by',
            'is_active',
            'skills',
            'job_description',
            'roles_and_responsibilities',
        ]

    def get_skills(self, obj):
        return [s.skill for s in obj.skills.all()]

    def get_job_description(self, obj):
        return [j.point for j in obj.job_descriptions.all()]

    def get_roles_and_responsibilities(self, obj):
        return [r.point for r in obj.roles_and_responsibilities.all()]

class JobApplicationSerializer(serializers.ModelSerializer):
    applicant = serializers.SerializerMethodField()

    class Meta:
        model = JobApplication
        fields = ['id', 'job', 'applicant', 'resume', 'applied_at', 'status']
        read_only_fields = ['id', 'job', 'applicant', 'applied_at', 'status']

    def get_applicant(self, obj):
        request = self.context.get('request')

        # Reuse the same profile serializer so HR can see full candidate info.
        user_data = UserProfileSerializer(obj.applicant, context={'request': request}).data

        return {
            'id': user_data.get('userId') or obj.applicant.userId,
            'uid': user_data.get('uid'),
            'fullname': user_data.get('fullname'),
            'email': user_data.get('email'),
            'role': user_data.get('role'),
            'company': user_data.get('company'),
            'phone': user_data.get('phone'),
            'location': user_data.get('location'),
            'bio': user_data.get('bio'),
            'profile_picture': user_data.get('profile_picture'),
            'experience': user_data.get('experience') or [],
            'skills': user_data.get('skills') or [],
            'job_preferences': user_data.get('job_preferences') or {},
            # Keep existing shape used by the frontend.
            'resume': {'required': True},
        }


class ReportSerializer(serializers.ModelSerializer):
    reporter = serializers.StringRelatedField()
    reviewed_by = serializers.StringRelatedField(allow_null=True)
    job_title = serializers.CharField(source='job.title', read_only=True)
    job_code = serializers.CharField(source='job.job_code', read_only=True)

    class Meta:
        model = Report
        fields = [
            'id', 'job', 'job_title', 'job_code', 'reporter', 'report_type',
            'reason', 'description', 'status', 'created_at',
            'reviewed_by', 'reviewed_at', 'action_taken'
        ]
        read_only_fields = ['id', 'reporter', 'created_at', 'reviewed_by', 'reviewed_at']


class ModerationLogSerializer(serializers.ModelSerializer):
    moderator = serializers.StringRelatedField()

    class Meta:
        model = ModerationLog
        fields = ['id', 'job', 'moderator', 'action', 'details', 'created_at']
        read_only_fields = ['id', 'moderator', 'created_at']


class UserStrikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()

    class Meta:
        model = UserStrike
        fields = ['id', 'user', 'reason', 'strike_level', 'created_at']
        read_only_fields = ['id', 'created_at']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id', 'type', 'title', 'message', 'is_read', 'created_at']
        read_only_fields = ['id', 'created_at']


class PermissionSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    user_id = serializers.IntegerField(source='user.userId', read_only=True)
    
    class Meta:
        model = Permission
        fields = ['id', 'user_id', 'user_email', 'permissions', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


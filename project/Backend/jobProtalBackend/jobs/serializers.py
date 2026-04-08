# serializers.py

from rest_framework import serializers
from .models import Job, JobSkill, JobDescription, JobResponsibility

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
            'id', 'title', 'company', 'location', 'experience',
            'type', 'salary', 'about_company', 'apply_source',
            'url', 'posted_at', 'posted_by',
            'skills', 'job_description', 'roles_and_responsibilities',
        ]
        
        read_only_fields = ['id', 'posted_by']  # these are set automatically, not by user input

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
            'title',
            'company',
            'location',
            'experience',
            'type',
            'salary',
            'about_company',
            'apply_source',
            'url',
            'posted_at',
            'posted_by',
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
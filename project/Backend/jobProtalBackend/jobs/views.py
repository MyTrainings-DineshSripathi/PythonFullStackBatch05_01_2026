# from django.shortcuts import render
# Create your views here.

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import JobSerializer, JobListSerializer
from .permissions import IsHR
from .models import Job, JobSkill, JobDescription, JobResponsibility
from django.utils import timezone
from datetime import timedelta


one_year_ago = timezone.now() - timedelta(days=365)

class PostJobView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes     = [IsHR]              # 👈 only HR gets through

    def post(self, request):
        serializer = JobSerializer(data=request.data)

        if serializer.is_valid():
            job = serializer.save(posted_by=request.user)  # 👈 track who posted
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
            posted_at__gte=one_year_ago     # 👈 gte = greater than or equal to
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
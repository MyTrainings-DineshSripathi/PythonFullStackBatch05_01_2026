from django.urls import path, include
from .views import PostJobView, getAllJobsView

urlpatterns = [
    path('post/', PostJobView.as_view(), name='post-job'),
    path('all/', getAllJobsView.as_view(), name='get-all-jobs'),
]
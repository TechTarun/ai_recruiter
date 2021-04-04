from django.urls import path, include
import api.candidate.urls
import api.company.urls
import api.job.urls

urlpatterns = [
  path('company/', include('api.company.urls')),
  path('candidate/', include('api.candidate.urls')),
  path('job/', include('api.job.urls')),
]
from django.urls import path, include
import api.candidate.urls
import api.company.urls
import api.job.urls
import api.hr.urls

urlpatterns = [
  path('company/', include('api.company.urls')),
  path('hr/', include('api.hr.urls')),
  path('candidate/', include('api.candidate.urls')),
  path('job/', include('api.job.urls')),
]
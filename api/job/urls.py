from django.urls import path
from .views import *

urlpatterns = [
  path('index', Index.as_view()),
  path('index/<str:id>', Index.as_view()),
  path('all', All.as_view()),
  path('apply', Apply.as_view()),
  path('filter', Filter.as_view()),
  path('visualization/<str:id>', Visualization.as_view()),
  path('interview', Interview.as_view()),
  # path('interview/<str:id>', Interview.as_view()),
]